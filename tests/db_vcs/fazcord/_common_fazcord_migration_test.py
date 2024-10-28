from typing import override

from tests.db_vcs.common_migration_test import CommonMigrationTest


class CommonFazcordMigrationTest:
    class Test(CommonMigrationTest.Test):

        @property
        @override
        def db_name(self) -> str:
            return "faz-cord_test"
