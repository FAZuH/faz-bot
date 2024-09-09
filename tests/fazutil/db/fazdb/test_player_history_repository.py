from datetime import datetime
from typing import override

from fazutil.db.fazdb.repository.player_history_repository import (
    PlayerHistoryRepository,
)
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestPlayerHistoryRepository(
    CommonFazdbRepositoryTest.Test[PlayerHistoryRepository]
):

    async def test_select_between_period(self) -> None:
        mocks = self._get_mock_data()
        mock1, mock2 = mocks[0], mocks[2]
        mock1.uuid = mock2.uuid
        mock1.datetime = datetime.fromtimestamp(10)
        mock2.datetime = datetime.fromtimestamp(100)
        await self.repo.insert([mock1, mock2])

        res = await self.repo.select_between_period(
            mock1.uuid, datetime.fromtimestamp(0), datetime.fromtimestamp(1000)
        )

        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], mock1)
        self.assertEqual(res[1], mock2)

    @override
    def _get_mock_data(self):
        return self._get_player_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.player_history_repository
