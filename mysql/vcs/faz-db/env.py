# Necessary to load the models
from typing import override

from sqlalchemy import MetaData

from fazutil.db.fazdb.fazdb_database import FazdbDatabase
from fazutil.db.fazdb.model.base_fazdb_model import BaseFazdbModel
from mysql.vcs.base_env import BaseEnv

FazdbDatabase  # type: ignore prevent being removed by linter lol


class FazdbEnv(BaseEnv):
    def __init__(self) -> None:
        self._metadata = BaseFazdbModel.metadata
        super().__init__()

    @property
    @override
    def metadata(self) -> MetaData:
        return self._metadata


env = FazdbEnv()
env.run()
