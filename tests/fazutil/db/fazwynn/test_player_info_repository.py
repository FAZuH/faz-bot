from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, override
from uuid import UUID

from fazutil.db.fazwynn.repository.player_info_repository import PlayerInfoRepository
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)

if TYPE_CHECKING:
    from fazutil.db.fazwynn.model.player_history import PlayerHistory


class TestPlayerInfoRepository(CommonFazwynnRepositoryTest.Test[PlayerInfoRepository]):
    async def test_safe_insert(self) -> None:
        """Test if safe_insert inserts PlayerInfo without corresponding GuildInfo
        without raising a constraint error
        """
        # Prepare
        mocks = self._get_mock_data()
        # Act
        await self.repo.safe_insert([mocks[0], mocks[2]])
        # Assert
        res = await self.repo.select_all()
        self.assertEqual(len(res), 2)
        res2 = await self.database.guild_info.select_all()
        self.assertEqual(len(res), 2)
        for r in res2:
            self.assertEqual(r.name, "-")
            self.assertEqual(r.prefix, "-")

    async def test_guild_relationship(self) -> None:
        # Prepare
        mock_bytes = UUID(int=0).bytes
        mock_guild_info = self._get_guild_info_mock_data()[0]
        mock_guild_info.uuid = mock_bytes
        await self.database.guild_info.insert(mock_guild_info)
        entity = self._get_mock_data()[0]
        entity.guild_uuid = mock_bytes
        await self.repo.insert(entity)
        res = await self.repo.select(entity.uuid)
        assert res
        # Act, Assert
        self.assertEqual(mock_guild_info, res.guild)

    async def test_get_player_no_match(self) -> None:
        # Act
        ret = await self.repo.get_player("abc")
        # Assert
        self.assertIsNone(ret)

    async def test_get_player_match_username(self) -> None:
        # Prepare
        entity = self._get_mock_data()[0]
        await self.repo.insert(entity)
        # Act
        res = await self.repo.get_player(entity.latest_username)
        # Assert
        self.assertEqual(res, entity)

    async def test_get_player_match_uuid(self) -> None:
        # Prepare
        entity = self._get_mock_data()[0]
        await self.repo.insert(entity)
        # Act
        res = await self.repo.get_player(entity.uuid)
        # Assert
        self.assertEqual(res, entity)

    async def __prepare_player_history(self) -> tuple[PlayerHistory, PlayerHistory]:
        mock_info = self._get_mock_data()[0]
        mocks_history = self._get_player_history_mock_data()

        mocksh1, mocksh2 = mocks_history[0], mocks_history[1]
        mocksh2.playtime += 1
        mocksh2.datetime = mocksh2.datetime + timedelta(seconds=10)
        mocksh2._compute_unique_id()

        await self.repo.insert(mock_info)
        await self.database.player_history.insert([mocksh1, mocksh2])
        return mocksh1, mocksh2

    async def test_latest_stat_relationship(self) -> None:
        # Prepare
        mocksh = (await self.__prepare_player_history())[1]

        # Act
        async with self.database.enter_async_session() as ses:
            res_info = await self.repo.select_all(session=ses)
            info = res_info[0]
            await info.awaitable_attrs.latest_stat
            self.assertEqual(info.latest_stat, mocksh)

    async def test_stat_history_relationship(self) -> None:
        # Prepare
        mocksh1, mocksh2 = await self.__prepare_player_history()

        # Act
        async with self.database.enter_async_session() as ses:
            res_info = await self.repo.select_all(session=ses)
            info = res_info[0]
            await info.awaitable_attrs.stat_history
            self.assertCountEqual(info.stat_history, [mocksh1, mocksh2])

    async def test_character_relationship(self) -> None:
        # Prepare
        mock_player = self._get_mock_data()[0]
        await self.repo.insert(mock_player)

        mock_ch = self._get_character_info_mock_data()[0]
        await self.database.character_info.insert(mock_ch)

        res = await self.repo.select(mock_player.uuid)
        assert res
        # Act, Assert
        self.assertEqual(mock_ch, res.characters[0])

    @override
    async def _create_table(self) -> None:
        self.database.create_all()

    @override
    def _get_mock_data(self):
        return self._get_player_info_mock_data()

    @property
    @override
    def repo(self):
        return self.database.player_info
