from typing import override

from fazutil.db.fazwynn.repository.guild_history_repository import (
    GuildHistoryRepository,
)
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)


class TestGuildHistoryRepository(
    CommonFazwynnRepositoryTest.Test[GuildHistoryRepository]
):
    @override
    async def _create_table(self) -> None:
        db = self.database
        db.create_all()
        mock_data = self._get_guild_info_mock_data()
        await db.guild_info.insert([mock_data[0], mock_data[2]])

    @override
    def _get_mock_data(self):
        return self._get_guild_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.guild_history
