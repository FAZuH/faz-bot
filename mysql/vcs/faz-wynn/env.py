# Necessary to load the models
from typing import override

from sqlalchemy import MetaData

from fazutil.db.fazwynn.fazwynn_database import FazwynnDatabase
from fazutil.db.fazwynn.model.base_fazwynn_model import BaseFazwynnModel
from mysql.vcs.base_env import BaseEnv

FazwynnDatabase  # type: ignore prevent being removed by linter lol


class FazdbEnv(BaseEnv):
    def __init__(self) -> None:
        self._metadata = BaseFazwynnModel.metadata
        super().__init__()

    @property
    @override
    def metadata(self) -> MetaData:
        return self._metadata

    @property
    @override
    def default_schema_env_name(self) -> str:
        return "MYSQL_FAZWYNN_DATABASE"


env = FazdbEnv()
env.run()
