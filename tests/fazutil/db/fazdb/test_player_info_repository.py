from typing import override
from uuid import UUID

from fazutil.db.fazdb.repository.player_info_repository import PlayerInfoRepository
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestPlayerInfoRepository(CommonFazdbRepositoryTest.Test[PlayerInfoRepository]):

    async def test_guild_relationship(self) -> None:
        # Prepare
        mock_bytes = UUID(int=0).bytes
        mock_guild_info = self._get_guild_info_mock_data()[0]
        mock_guild_info.uuid = mock_bytes
        await self.database.guild_info_repository.insert(mock_guild_info)
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

    @override
    async def _create_table(self) -> None:
        await self.database.guild_info_repository.create_table()
        await self.database.player_info_repository.create_table()

    @override
    def _get_mock_data(self):
        return self._get_player_info_mock_data()

    @property
    @override
    def repo(self):
        return self.database.player_info_repository
