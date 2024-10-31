from typing import override

from fazutil.db.fazwynn.repository.guild_member_history_repository import (
    GuildMemberHistoryRepository,
)
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)


class TestGuildMemberHistoryRepository(
    CommonFazwynnRepositoryTest.Test[GuildMemberHistoryRepository]
):
    @override
    def _get_mock_data(self):
        return self._get_guild_member_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.guild_member_history
