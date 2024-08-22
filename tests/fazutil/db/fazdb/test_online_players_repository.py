from typing import override

from fazutil.db.fazdb.repository.online_players_repository import (
    OnlinePlayersRepository,
)
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestOnlinePlayersRepository(
    CommonFazdbRepositoryTest.Test[OnlinePlayersRepository]
):

    @override
    def _get_mock_data(self):
        return self._get_online_players_mock_data()

    @property
    @override
    def repo(self):
        return self.database.online_players_repository
