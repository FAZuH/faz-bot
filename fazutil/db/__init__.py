from typing import TYPE_CHECKING

from .fazbot import FazbotDatabase
from .fazdb import FazdbDatabase


if TYPE_CHECKING:
    from .base_database import BaseDatabase
    from .base_mysql_database import BaseMySQLDatabase
    from .base_model import BaseModel
    from .base_repository import BaseRepository
