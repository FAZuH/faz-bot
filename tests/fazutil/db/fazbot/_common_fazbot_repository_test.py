from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, override

from fazutil.db.fazbot import FazbotDatabase

from .._common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazutil.db.base_repository import BaseRepository


class CommonFazbotRepositoryTest:

    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[FazbotDatabase, R], ABC):

        @property
        @override
        def database_type(self) -> type[FazbotDatabase]:
            return FazbotDatabase

        @property
        def db_name(self) -> str:
            """Database name to be tested."""
            return "faz-bot_test"
