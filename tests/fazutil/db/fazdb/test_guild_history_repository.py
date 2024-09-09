from typing import override

from fazutil.db.fazdb.repository.guild_history_repository import GuildHistoryRepository
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestGuildHistoryRepository(
    CommonFazdbRepositoryTest.Test[GuildHistoryRepository]
):
    @override
    def _get_mock_data(self):
        return self._get_guild_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.guild_history
