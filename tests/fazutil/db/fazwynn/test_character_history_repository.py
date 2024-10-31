from typing import override

from fazutil.db.fazwynn.repository.character_history_repository import (
    CharacterHistoryRepository,
)
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)


class TestCharacterHistoryRepository(
    CommonFazwynnRepositoryTest.Test[CharacterHistoryRepository]
):
    @override
    async def _create_table(self) -> None:
        db = self.database
        db.create_all()

        mock_player = self._get_player_info_mock_data()
        mock_char = self._get_character_info_mock_data()

        await self.database.player_info.insert([mock_player[0], mock_player[2]])
        await self.database.character_info.insert([mock_char[0], mock_char[2]])

    @override
    def _get_mock_data(self):
        return self._get_character_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.character_history
