from datetime import datetime as dt

from sqlalchemy import Index
from sqlalchemy.dialects.mysql import BINARY, DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from fazutil.db.fazdb.model.base_fazdb_model import BaseFazdbModel


class PlayerActivityHistory(BaseFazdbModel):
    __tablename__ = "player_activity_history"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), nullable=False, primary_key=True)
    logon_datetime: Mapped[dt] = mapped_column(
        DATETIME, nullable=False, primary_key=True
    )
    logoff_datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False)

    __table_args__ = (
        Index(None, logon_datetime.desc()),
        Index(None, logoff_datetime.desc()),
    )
