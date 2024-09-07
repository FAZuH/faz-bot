from __future__ import annotations

import unittest
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any, override

from sqlalchemy import inspect

from fazutil.db.base_model import BaseModel
from fazutil.properties import Properties

if TYPE_CHECKING:
    from sqlalchemy import Connection

    from fazutil.db.base_mysql_database import BaseMySQLDatabase
    from fazutil.db.base_repository import BaseRepository


class CommonDbRepositoryTest:

    # HACK: Nesting test classes like this prevents CommonDbRepositoryTest.Test from being discovered by unittest.
    class Test[DB: BaseMySQLDatabase, R: BaseRepository[BaseModel, Any]](
        unittest.IsolatedAsyncioTestCase, ABC
    ):

        @override
        async def asyncSetUp(self) -> None:
            Properties.setup()
            self._database = self.database_type(
                Properties.MYSQL_USERNAME,
                Properties.MYSQL_PASSWORD,
                Properties.MYSQL_HOST,
                Properties.MYSQL_PORT,
                self.db_name,
            )
            self._database.drop_all()
            await self._create_table()

        async def test_insert_successful(self) -> None:
            """Test if insert inserts an entry successfully and properly to table."""
            # Prepare
            mock_data0 = self._get_mock_data()[0]
            # Act
            await self.repo.insert(mock_data0)
            # Assert
            rows = await self.repo.select_all()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0], mock_data0)

        async def test_insert_successful_many_entries(self) -> None:
            """Test if insert inserts many entries successfully and properly to table."""
            # Prepare
            mock_data = self._get_mock_data()
            to_insert = (mock_data[0], mock_data[2])
            # Act
            await self.repo.insert(to_insert)
            # Assert
            rows = await self.repo.select_all()
            self.assertEqual(len(rows), 2)
            self.assertSetEqual(set(rows), set(to_insert))

        async def test_insert_ignore_on_duplicate(self) -> None:
            """Test if insert inserts entries properly
            with ignore_on_duplicate argument set to True."""
            # Prepare
            mock_data = self._get_mock_data()
            await self.repo.insert(mock_data[0])
            # Act: Insert the same data again. This shouldn't insert.
            await self.repo.insert(mock_data[0], ignore_on_duplicate=True)
            # Assert
            rows = await self.repo.select_all()
            self.assertEqual(len(rows), 1)
            self.assertSetEqual(set(rows), set((mock_data[0],)))

        async def test_insert_replace_on_duplicate(self) -> None:
            """Test if insert replace duplicate entries properly
            with replace_on_duplicate argument set to True."""
            # Prepare
            mock_data = self._get_mock_data()
            await self.repo.insert(mock_data[0])
            # Act: Insert the same data again. This should replace previous insert
            await self.repo.insert(mock_data[3], replace_on_duplicate=True)
            # Assert
            rows = await self.repo.select_all()
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row, mock_data[3])

        async def test_insert_replace_specific_column(self) -> None:
            """Test if insert with columns_to_replace set properly replaces
            values of specified columns."""
            # Prepare
            mock_data = self._get_mock_data()
            modified_column_name = mock_data[-1]
            await self.repo.insert(mock_data[0])
            # Act: Insert the same data again. This should replace previous insert
            await self.repo.insert(
                mock_data[3],
                replace_on_duplicate=True,
                columns_to_replace=[modified_column_name],
            )
            # Assert: that only columns specified by 'columns_to_replace' was changed
            rows = await self.repo.select_all()
            self.assertEqual(len(rows), 1)
            row = rows[0]
            non_modified_values_lambda = lambda x: {
                k: v for k, v in x.to_dict().items() if k != modified_column_name
            }
            modified_values_lambda = lambda x: {
                k: v for k, v in x.to_dict().items() if k == modified_column_name
            }
            self.assertEqual(
                non_modified_values_lambda(row),
                non_modified_values_lambda(mock_data[3]),
            )
            self.assertNotEqual(
                modified_values_lambda(row), modified_values_lambda(mock_data[0])
            )

        async def test_delete_successful(self) -> None:
            """Test if delete deletes the specified entry properly."""
            # Prepare
            mock_data = self._get_mock_data()
            await self.repo.insert(mock_data[0])
            id_ = self._get_value_of_primary_key(mock_data[0])
            # Act
            await self.repo.delete(id_)
            # Assert
            rows = await self.repo.select_all()
            self.assertEqual(len(rows), 0)

        async def test_is_exists_should_return_true(self) -> None:
            """Test if is_exist returns true if specified entry exist."""
            # Prepare
            mock_data = self._get_mock_data()
            mock_data0 = mock_data[0]
            await self.repo.insert(mock_data0)
            id_ = self._get_value_of_primary_key(mock_data0)
            # Act
            is_exists = await self.repo.is_exists(id_)
            # Assert
            self.assertTrue(is_exists)

        async def test_is_exists_should_return_false(self) -> None:
            """Test if is_exist returns false if specified entry doesn't exist."""
            # Prepare
            mock_data = self._get_mock_data()
            id2 = self._get_value_of_primary_key(mock_data[2])
            # Act
            is_exist2 = await self.repo.is_exists(id2)
            # Assert
            self.assertFalse(is_exist2)

        async def test_select_all_successful(self) -> None:
            """Test select_all returns all entries."""
            # Prepare
            mock_data = self._get_mock_data()
            await self.repo.insert([mock_data[0], mock_data[2]])
            # Act
            res = await self.repo.select_all()
            # Assert
            self.assertEqual(len(res), 2)
            self.assertSetEqual(set(res), {mock_data[0], mock_data[2]})

        @override
        async def asyncTearDown(self) -> None:
            self.database.drop_all()
            await self.database.async_engine.dispose()

        def _get_value_of_primary_key(self, entity: BaseModel) -> Any:
            pk_columns = inspect(self.repo.model).primary_key
            if len(pk_columns) == 1:
                col_ = pk_columns[0]
                value = getattr(entity, col_.name)
                return value
            values = [getattr(entity, col.name) for col in pk_columns]
            return values  # type: ignore

        @staticmethod
        def _get_table_names(connection: Connection) -> list[str]:
            inspector = inspect(connection)
            return inspector.get_table_names()

        @staticmethod
        def _get_mock_datetime() -> datetime:
            return datetime.now().replace(microsecond=0)

        @property
        def database(self) -> DB:
            return self._database

        async def _create_table(self) -> None:
            """Method to create table safely. Override this method when the
            table being tested requires additional tables to be created first."""
            await self.repo.create_table()

        @abstractmethod
        def _get_mock_data(
            self,
        ) -> tuple[BaseModel, BaseModel, BaseModel, BaseModel, Any]:
            """Create tuple of mock data to be tested by test methods.
            Second mock data is a duplicate of the first.
            Third mock data is duplicate of first with different primary key value.
            Fourth mock data is duplicate of first, with different value on columns with no unique constraints.
            5th element of the tuple is the column name that was modified on fourth mock data.

            Returns
            -------
            tuple[T, ...]
                Mock test data.
            """
            ...

        @property
        @abstractmethod
        def database_type(self) -> type[DB]:
            """Database class to test."""
            ...

        @property
        @abstractmethod
        def repo(self) -> R:
            """Repository object to test tested."""
            ...

        @property
        @abstractmethod
        def db_name(self) -> str:
            """Database name to tset."""
            ...
