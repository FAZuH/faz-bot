from typing import override

from fazutil.db.fazdb.repository.fazdb_uptime_repository import FazdbUptimeRepository
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)


class TestFazdbUptimeRepository(CommonFazdbRepositoryTest.Test[FazdbUptimeRepository]):
    @override
    def _get_mock_data(self):
        return self._get_fazdb_uptime_mock_data()

    @property
    @override
    def repo(self):
        return self.database.fazdb_uptime
