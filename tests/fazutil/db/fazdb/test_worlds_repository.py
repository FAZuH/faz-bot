from datetime import datetime
from typing import override

from fazutil.db.fazdb.repository import WorldsRepository

from ._common_fazdb_repository_test import CommonFazdbRepositoryTest


class TestWorldsRepository(CommonFazdbRepositoryTest.Test[WorldsRepository]):

    async def test_update_worlds(self) -> None:
        """Test if update_words properly update worlds. Deletes worlds that's
        not up anymore, and updates player_count for worlds that's still up

        1. Insert with mock data: WC1, WC3
        2. update_worlds(WC2, WC3) mock data:
          - WC1 went down
          - WC2 went up
          - WC3 stays the same
        3. Assert
          - WC1 no longer on table
          - WC2 is on table
          - WC3 player_count is updated
        """
        # Prepare
        mock = self._get_mock_data()
        w1 = mock[0]
        w2 = mock[2]
        w3 = w2.clone()
        w3.name = "WC3"
        await self.repo.insert([w1, w3])
        wc3_future = w3.clone()
        wc3_future.player_count = 40
        # Act
        await self.repo.update_worlds([w2, wc3_future])
        # Assert
        rows = await self.repo.select_all()
        self.assertEqual(len(rows), 2)
        self.assertNotIn(w1, rows)
        self.assertIn(w2, rows)
        for row in rows:
            if row.name != w3.name:
                continue
            self.assertEqual(wc3_future.player_count, row.player_count)

    async def test_get_worlds_sorted_time(self) -> None:
        # Prepare
        w1, w2, w3, w4, _ = self._get_mock_data()
        w1.name = "WC1"
        w2.name = "WC2"
        w3.name = "WC3"
        w4.name = "WC4"
        w1.time_created = datetime(2000, 1, 1)
        w2.time_created = datetime(2000, 1, 2)
        w3.time_created = datetime(2000, 1, 3)
        w4.time_created = datetime(2000, 1, 4)
        await self.repo.insert([w1, w2, w3, w4])
        # Act
        res = await self.repo.get_worlds()
        # Assert
        res[0].time_created = w4.time_created
        res[1].time_created = w3.time_created
        res[2].time_created = w2.time_created
        res[3].time_created = w1.time_created

    async def test_get_worlds_sorted_player(self) -> None:
        # Prepare
        w1, w2, w3, w4, _ = self._get_mock_data()
        w1.name = "WC1"
        w2.name = "WC2"
        w3.name = "WC3"
        w4.name = "WC4"
        w1.player_count = 1
        w2.player_count = 2
        w3.player_count = 3
        w4.player_count = 4
        await self.repo.insert([w1, w2, w3, w4])
        # Act
        res = await self.repo.get_worlds()
        # Assert
        res[0].player_count = w1.player_count
        res[1].player_count = w2.player_count
        res[2].player_count = w3.player_count
        res[3].player_count = w4.player_count

    @override
    def _get_mock_data(self):
        return self._get_worlds_mock_data()

    @property
    @override
    def repo(self):
        return self.database.worlds_repository
