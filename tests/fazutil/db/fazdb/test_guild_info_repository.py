from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, override
from uuid import UUID

from fazutil.db.fazdb.repository.guild_info_repository import GuildInfoRepository
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)

if TYPE_CHECKING:
    from fazutil.db.fazdb.model.guild_history import GuildHistory


class TestGuildInfoRepository(CommonFazdbRepositoryTest.Test[GuildInfoRepository]):
    async def test_members_relationship(self) -> None:
        # Prepare
        mock_bytes = UUID(int=0).bytes
        entity = self._get_mock_data()[0]
        entity.uuid = mock_bytes
        await self.repo.insert(entity)
        mock_players = self._get_player_info_mock_data()
        player1 = mock_players[0]
        player2 = mock_players[2]
        player1.guild_uuid = mock_bytes
        player2.guild_uuid = mock_bytes
        await self.database.player_info.insert([player1, player2])
        # Act, Assert
        res = await self.repo.select(entity.uuid)
        assert res
        self.assertIn(player1, res.members)
        self.assertIn(player2, res.members)

    async def __prepare_guild_history(self) -> tuple[GuildHistory, GuildHistory]:
        mock_info = self._get_mock_data()[0]
        mocks_history = self._get_guild_history_mock_data()

        mocksh1, mocksh2 = mocks_history[0], mocks_history[1]
        mocksh2.level += 1
        mocksh2.datetime = mocksh2.datetime + timedelta(seconds=10)
        mocksh2._compute_unique_id()

        await self.repo.insert(mock_info)
        await self.database.guild_history.insert([mocksh1, mocksh2])
        return mocksh1, mocksh2

    async def test_latest_stat_relationship(self) -> None:
        # Prepare
        mocksh = (await self.__prepare_guild_history())[1]

        # Act
        async with self.database.enter_async_session() as ses:
            res_info = await self.repo.select_all(session=ses)
            info = res_info[0]
            await info.awaitable_attrs.latest_stat
            self.assertEqual(info.latest_stat, mocksh)

    async def test_stat_history_relationship(self) -> None:
        # Prepare
        mocksh1, mocksh2 = await self.__prepare_guild_history()

        # Act
        async with self.database.enter_async_session() as ses:
            res_info = await self.repo.select_all(session=ses)
            info = res_info[0]
            await info.awaitable_attrs.stat_history
            self.assertCountEqual(info.stat_history, [mocksh1, mocksh2])

    @override
    async def _create_table(self) -> None:
        self.database.create_all()

    @override
    def _get_mock_data(self):
        return self._get_guild_info_mock_data()

    @property
    @override
    def repo(self):
        return self.database.guild_info
