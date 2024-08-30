from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, override

from fazutil.db.fazcord.fazcord_database import FazcordDatabase
from tests.fazutil.db._common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazutil.db.base_repository import BaseRepository


class CommonFazcordRepositoryTest:

    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[FazcordDatabase, R], ABC):

        @property
        @override
        def database_type(self) -> type[FazcordDatabase]:
            return FazcordDatabase

        @property
        def db_name(self) -> str:
            """Database name to be tested."""
            return "faz-cord_test"
