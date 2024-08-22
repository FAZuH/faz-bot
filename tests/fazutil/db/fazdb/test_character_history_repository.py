from typing import override

from fazutil.db.fazdb.repository.character_history_repository import (
    CharacterHistoryRepository,
)
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestCharacterHistoryRepository(
    CommonFazdbRepositoryTest.Test[CharacterHistoryRepository]
):

    @override
    def _get_mock_data(self):
        return self._get_character_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.character_history_repository
