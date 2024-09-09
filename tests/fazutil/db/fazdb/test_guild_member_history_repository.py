from typing import override

from fazutil.db.fazdb.repository.guild_member_history_repository import (
    GuildMemberHistoryRepository,
)
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestGuildMemberHistoryRepository(
    CommonFazdbRepositoryTest.Test[GuildMemberHistoryRepository]
):
    @override
    def _get_mock_data(self):
        return self._get_guild_member_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.guild_member_history
