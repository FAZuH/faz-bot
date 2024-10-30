from datetime import datetime
from typing import override

from fazutil.db.fazwynn.repository.player_history_repository import (
    PlayerHistoryRepository,
)
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)


class TestPlayerHistoryRepository(
    CommonFazwynnRepositoryTest.Test[PlayerHistoryRepository]
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
    async def _create_table(self) -> None:
        db = self.database
        db.create_all()
        mock_data = self._get_player_info_mock_data()
        await db.player_info.insert([mock_data[0], mock_data[2]])

    @override
    def _get_mock_data(self):
        return self._get_player_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.player_history