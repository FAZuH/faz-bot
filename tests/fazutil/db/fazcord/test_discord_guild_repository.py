from typing import override

from fazutil.db.fazcord.repository.discord_guild_repository import DiscordGuildRepository
from tests.fazutil.db.fazcord._common_fazcord_repository_test import (
    CommonFazcordRepositoryTest,
)


class TestDiscordGuildRepository(
    CommonFazcordRepositoryTest.Test[DiscordGuildRepository]
):

    @override
    def _get_mock_data(self):
        model = self.repo.model
        mock_data1 = model(guild_id=1, guild_name="a")
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.guild_id = 2
        mock_data4 = mock_data1.clone()
        mock_data4.guild_name = "b"
        return (mock_data1, mock_data2, mock_data3, mock_data4, "guild_name")

    @property
    @override
    def repo(self):
        return self.database.discord_guild_repository
