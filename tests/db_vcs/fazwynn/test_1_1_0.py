from typing import override

from tests.db_vcs.fazwynn._common_fazwynn_migration_test import CommonFazdbMigrationTest


class Test_1_1_0(CommonFazdbMigrationTest.Test):

    @property
    @override
    def target_version(self) -> str:
        return "3173276fb06a"
