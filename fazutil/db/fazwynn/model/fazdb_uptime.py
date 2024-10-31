from datetime import datetime as dt

from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from fazutil.db.fazwynn.model.base_fazwynn_model import BaseFazwynnModel


class FazdbUptime(BaseFazwynnModel):
    __tablename__ = "fazdb_uptime"

    start_time: Mapped[dt] = mapped_column(DATETIME, primary_key=True, nullable=False)
    stop_time: Mapped[dt] = mapped_column(DATETIME, nullable=False)
