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
    @override
    def _get_mock_data(self):
        return self._get_character_info_mock_data()

    @property
    @override
    def repo(self):
        return self.database.character_info_repository
