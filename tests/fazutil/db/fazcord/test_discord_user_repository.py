from typing import override

from fazutil.db.fazcord.repository.discord_user_repository import DiscordUserRepository
from tests.fazutil.db.fazcord._common_fazcord_repository_test import (
    CommonFazcordRepositoryTest,
)


class TestDiscordUserRepository(
    CommonFazcordRepositoryTest.Test[DiscordUserRepository]
):

    @override
    async def _create_table(self) -> None:
        await self.database.discord_guild_repository.create_table()
        await self.database.discord_user_repository.create_table()
        await self.database.discord_channel_repository.create_table()
        await self.database.track_entry_repository.create_table()

    @override
    def _get_mock_data(self):
        return self._get_discord_user_mock_data()

    @property
    @override
    def repo(self):
        return self.database.discord_user_repository
