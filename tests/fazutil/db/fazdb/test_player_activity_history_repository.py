from __future__ import annotations

from datetime import datetime
from typing import override

from fazutil.db.fazdb.repository.player_activity_history_repository import (
    PlayerActivityHistoryRepository,
)
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestPlayerActivityHistoryRepository(
    CommonFazdbRepositoryTest.Test[PlayerActivityHistoryRepository]
):
    async def test_select_between_period(self) -> None:
        # Prepare
        e1, e2, e3, e4, _ = self._get_mock_data()
        e1.logon_datetime = datetime.fromtimestamp(100)
        e1.logoff_datetime = datetime.fromtimestamp(200)
        e2.uuid = e1.uuid
        e2.logon_datetime = datetime.fromtimestamp(300)
        e2.logoff_datetime = datetime.fromtimestamp(400)
        e3.uuid = e1.uuid
        e3.logon_datetime = datetime.fromtimestamp(500)
        e3.logoff_datetime = datetime.fromtimestamp(600)
        e4.uuid = e1.uuid
        e4.logon_datetime = datetime.fromtimestamp(700)
        e4.logoff_datetime = datetime.fromtimestamp(800)
        e5 = e4.clone()
        e5.logon_datetime = datetime.fromtimestamp(900)
        e5.logoff_datetime = datetime.fromtimestamp(1000)
        # for e in [e1, e2, e3, e4]:
        #     logger.debug(
        #         f"{e.logon_datetime.timestamp()} - {e.logoff_datetime.timestamp()}"
        #     )
        await self.repo.insert([e1, e2, e3, e4, e5])
        # Act
        playtime1 = await self.repo.get_playtime_between_period(
            e1.uuid,
            datetime.fromtimestamp(0),
            datetime.fromtimestamp(1000),
        )
        playtime2 = await self.repo.get_playtime_between_period(
            e1.uuid,
            datetime.fromtimestamp(350),
            datetime.fromtimestamp(750),
        )
        # for e in entities1:
        #     logger.debug(
        #         f"{e.logon_datetime.timestamp()} - {e.logoff_datetime.timestamp()}"
        #     )
        # Assert
        self.assertAlmostEqual(playtime1.total_seconds(), 500)
        self.assertAlmostEqual(playtime2.total_seconds(), 200)

    @override
    def _get_mock_data(self):
        return self._get_player_activity_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.player_activity_history_repository
