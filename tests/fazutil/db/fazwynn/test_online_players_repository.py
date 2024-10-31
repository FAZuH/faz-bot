from typing import override

from fazutil.db.fazwynn.repository.online_players_repository import (
    OnlinePlayersRepository,
)
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)


class TestOnlinePlayersRepository(
    CommonFazwynnRepositoryTest.Test[OnlinePlayersRepository]
):
    @override
    def _get_mock_data(self):
        return self._get_online_players_mock_data()

    @property
    @override
    def repo(self):
        return self.database.online_players
