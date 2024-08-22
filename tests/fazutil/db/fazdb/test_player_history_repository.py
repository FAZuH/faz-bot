from typing import override

from fazutil.db.fazdb.repository import PlayerHistoryRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestPlayerHistoryRepository(
    CommonFazdbRepositoryTest.Test[PlayerHistoryRepository]
):

    @override
    def _get_mock_data(self):
        return self._get_player_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.player_history_repository
