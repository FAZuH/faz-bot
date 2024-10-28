from typing import override

from tests.db_vcs.fazcord._common_fazcord_migration_test import (
    CommonFazcordMigrationTest,
)


class Test_1_0_0(CommonFazcordMigrationTest.Test):

    @property
    @override
    def target_version(self) -> str:
        return "305fa6683a43"
