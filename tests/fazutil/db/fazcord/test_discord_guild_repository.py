from typing import override

from fazutil.db.fazcord.repository.discord_guild_repository import (
    DiscordGuildRepository,
)
from tests.fazutil.db.fazcord._common_fazcord_repository_test import (
    CommonFazcordRepositoryTest,
)


class TestDiscordGuildRepository(
    CommonFazcordRepositoryTest.Test[DiscordGuildRepository]
):
    @override
    async def _create_table(self) -> None:
        await self.database.discord_guild.create_table()
        await self.database.discord_user.create_table()
        await self.database.discord_channel.create_table()
        await self.database.track_entry.create_table()

    @override
    def _get_mock_data(self):
        return self._get_discord_guild_mock_data()

    @property
    @override
    def repo(self):
        return self.database.discord_guild
