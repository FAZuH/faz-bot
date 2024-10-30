from datetime import datetime

from sqlalchemy.dialects.mysql import DATETIME, SMALLINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from fazutil.db.fazwynn.model.base_fazwynn_model import BaseFazwynnModel


class Worlds(BaseFazwynnModel):
    __tablename__ = "worlds"

    name: Mapped[str] = mapped_column(VARCHAR(16), nullable=False, primary_key=True)
    player_count: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    time_created: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
