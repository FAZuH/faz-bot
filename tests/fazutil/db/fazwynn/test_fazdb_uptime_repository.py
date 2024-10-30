from typing import override

from fazutil.db.fazwynn.repository.fazdb_uptime_repository import FazdbUptimeRepository
from tests.fazutil.db.fazwynn._common_fazwynn_repository_test import (
    CommonFazwynnRepositoryTest,
)


class TestFazdbUptimeRepository(
    CommonFazwynnRepositoryTest.Test[FazdbUptimeRepository]
):
    @override
    def _get_mock_data(self):
        return self._get_fazdb_uptime_mock_data()

    @property
    @override
    def repo(self):
        return self.database.fazdb_uptime
