from datetime import datetime, timedelta
from typing import override

import pandas

from fazutil.db.fazwynn.repository.player_history_repository import (
    PlayerHistoryRepository,
)
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)


class TestPlayerHistoryRepository(
    CommonFazwynnRepositoryTest.Test[PlayerHistoryRepository]
):

    async def test_select_between_period_returns_within_range(self) -> None:
        # Prepare
        self.__insert_mock_player_history()
        since = self._get_mock_datetime() - timedelta(days=100)
        until = self._get_mock_datetime() + timedelta(days=100)
        mock = self._get_mock_data()[0]

        # Act
        res = await self.repo.select_between_period(mock.uuid, since, until)

        # Assert
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], mock)

    async def test_select_between_period_returns_empty_when_outside_range(self) -> None:
        # Prepare
        self.__insert_mock_player_history()
        since = datetime.fromtimestamp(0)
        until = datetime.fromtimestamp(100)
        mock = self._get_mock_data()[0]

        # Act
        res = await self.repo.select_between_period(mock.uuid, since, until)

        # Assert
        self.assertEqual(len(res), 0)

    async def test_select_between_period_as_dataframe_returns_within_range(
        self,
    ) -> None:
        # Prepare
        self.__insert_mock_player_history()
        since = self._get_mock_datetime() - timedelta(days=100)
        until = self._get_mock_datetime() + timedelta(days=100)
        mock = self._get_mock_data()[0]

        # Act
        res = self.repo.select_between_period_as_dataframe(mock.uuid, since, until)

        # Assert
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res, pandas.DataFrame)
        self.assertEqual(res.iloc[0].to_dict(), mock.to_dict())

    async def test_select_between_period_as_dataframe_returns_empty_when_outside_range(
        self,
    ) -> None:
        # Prepare
        self.__insert_mock_player_history()
        since = datetime.fromtimestamp(0)
        until = datetime.fromtimestamp(100)
        mock = self._get_mock_data()[0]

        # Act
        res = self.repo.select_between_period_as_dataframe(mock.uuid, since, until)

        # Assert
        self.assertEqual(len(res), 0)

    def __insert_mock_player_history(self):
        mock = self._get_mock_data()[0]
        with self.database.enter_session() as ses:
            ses.add(mock)

    @override
    async def _create_table(self) -> None:
        db = self.database
        db.create_all()
        mock_data = self._get_player_info_mock_data()
        await db.player_info.insert([mock_data[0], mock_data[2]])

    @override
    def _get_mock_data(self):
        return self._get_player_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.player_history
