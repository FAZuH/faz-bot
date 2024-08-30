from typing import override

from fazutil.db.fazcord.repository.discord_user_repository import DiscordUserRepository
from tests.fazutil.db.fazcord._common_fazcord_repository_test import (
    CommonFazcordRepositoryTest,
)


class TestDiscordUserRepository(CommonFazcordRepositoryTest.Test[DiscordUserRepository]):

    @override
    def _get_mock_data(self):
        model = self.repo.model
        mock_data1 = model(user_id=1, username="a")
        mock_data2 = mock_data1.clone()
        mock_data3 = mock_data1.clone()
        mock_data3.user_id = 2
        mock_data4 = mock_data1.clone()
        mock_data4.username = "b"
        return (mock_data1, mock_data2, mock_data3, mock_data4, "username")

    @property
    @override
    def repo(self):
        return self.database.discord_user_repository
