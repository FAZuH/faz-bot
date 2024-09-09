from typing import override

from fazutil.db.fazdb.repository.character_info_repository import (
    CharacterInfoRepository,
)
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestCharacterInfoRepository(
    CommonFazdbRepositoryTest.Test[CharacterInfoRepository]
):
    async def test_select_from_player(self) -> None:
        await self.database.guild_info.create_table()
        await self.database.player_info.create_table()
        mock_player = self._get_player_info_mock_data()[0]
        mock_characters = self._get_mock_data()
        char1, char2 = mock_characters[0], mock_characters[2]
        char1.uuid = char2.uuid = mock_player.uuid
        await self.database.player_info.safe_insert(mock_player)
        await self.repo.insert([char1, char2])

        res = await self.repo.select_from_player(mock_player.uuid)

        self.assertIn(char1, res)
        self.assertIn(char2, res)

    @override
    def _get_mock_data(self):
        return self._get_character_info_mock_data()

    @property
    @override
    def repo(self):
        return self.database.character_info
