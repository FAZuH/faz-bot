from typing import override
from uuid import UUID

from fazutil.db.fazdb.repository import GuildInfoRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


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
        await self.database.player_info_repository.insert([player1, player2])
        # Act, Assert
        res = await self.repo.select(entity.uuid)
        assert res
        self.assertIn(player1, res.members)
        self.assertIn(player2, res.members)

    @override
    async def _create_table(self) -> None:
        await self.repo.create_table()
        await self.database.player_info_repository.create_table()

    @override
    def _get_mock_data(self):
        return self._get_guild_info_mock_data()

    @property
    @override
    def repo(self):
        return self.database.guild_info_repository
