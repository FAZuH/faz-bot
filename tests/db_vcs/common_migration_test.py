import io
import os
from abc import ABC, abstractmethod
from typing import override
from unittest import TestCase

from alembic import command
from alembic.config import Config
from alembic.environment import EnvironmentContext
from alembic.script.base import ScriptDirectory
from sqlalchemy import engine_from_config, text


class CommonMigrationTest:
    class Test(TestCase, ABC):

        @override
        def setUp(self) -> None:
            self._output_buffer = io.StringIO()
            self.alembic_cfg = Config(
                "alembic.ini", self.db_name, stdout=self._output_buffer
            )

            self.__drop_all()
            command.stamp(self.alembic_cfg, self.start_version)

        def test_upgrade(self):
            # Act
            command.upgrade(self.alembic_cfg, self.target_version)

            # Assert
            command.current(self.alembic_cfg)

            output = self._output_buffer.getvalue()
            self.assertIn(self.target_version, output)

        def test_downgrade(self):
            # Prepare
            command.upgrade(self.alembic_cfg, self.target_version)

            # Act
            command.downgrade(self.alembic_cfg, self.start_version)

            output = self._output_buffer.getvalue()
            self.assertEqual(output, "")

        @override
        def tearDown(self) -> None:
            command.stamp(self.alembic_cfg, self.start_version)

        # def _populate_db(self) -> None:
        #     test = CommonFazdbRepositoryTest.Test
        #     mocks = []
        #     mocks.append(test._get_fazdb_uptime_mock_data())
        #     mocks.append(test._get_guild_info_mock_data())
        #     mocks.append(test._get_guild_member_history_mock_data())
        #     mocks.append(test._get_online_players_mock_data())
        #     mocks.append(test._get_player_activity_history_mock_data())
        #     mocks.append(test._get_worlds_mock_data())
        #     mocks.append(test._get_guild_history_mock_data())
        #     mocks.append(test._get_player_info_mock_data())
        #     mocks.append(test._get_character_info_mock_data())
        #     mocks.append(test._get_player_history_mock_data())
        #     mocks.append(test._get_character_history_mock_data())
        #
        #     with self._db.must_enter_session() as ses:
        #         for mock in mocks:
        #             ses.add_all([mock[0], mock[2]])

        @property
        def start_version(self) -> str:
            return "base"

        def __get_url(self):
            """Override sqlalchemy.url with environment variables if set"""
            user = os.getenv("MYSQL_USER", None)
            password = os.getenv("MYSQL_PASSWORD", None)
            host = os.getenv("MYSQL_HOST", None)
            db_name = os.getenv("MYSQL_FAZCORD_DATABASE", None)

            if None in {user, password, host, db_name}:
                section = self.alembic_cfg.get_section(
                    self.alembic_cfg.config_ini_section
                )
                assert section is not None
                return section["sqlalchemy.url"]

            return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

        def __drop_all(self):
            section = self.alembic_cfg.get_section(self.alembic_cfg.config_ini_section)
            assert section
            section["sqlalchemy.url"] = self.__get_url()

            engine = engine_from_config(section, prefix="sqlalchemy.")
            with engine.connect() as conn:
                # Get environment context
                env = EnvironmentContext(
                    self.alembic_cfg, ScriptDirectory.from_config(self.alembic_cfg)
                )
                env.configure(conn)

                # Create a context manager that provides the connection
                with env.begin_transaction():
                    # First, disable foreign key checks
                    conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))

                    # Get the drop statements
                    result = conn.execute(
                        text(
                            """
                            SELECT 
                                CONCAT('DROP TABLE IF EXISTS `', table_name, '`')
                            FROM information_schema.tables
                            WHERE table_schema = DATABASE()
                            AND table_type = 'BASE TABLE'
                        """
                        )
                    )

                    # Execute each drop statement
                    for (drop_statement,) in result:
                        conn.execute(text(drop_statement))

                    # Re-enable foreign key checks
                    conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))

        @property
        @abstractmethod
        def target_version(self) -> str: ...

        @property
        @abstractmethod
        def db_name(self) -> str:
            """Database name to test."""
            ...
