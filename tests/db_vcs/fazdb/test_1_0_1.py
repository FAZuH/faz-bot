from typing import override

from tests.db_vcs.fazdb._common_fazdb_migration_test import CommonFazdbMigrationTest


class Test_1_0_1(CommonFazdbMigrationTest.Test):

    @property
    @override
    def target_version(self) -> str:
        return "3965042b4d49"
