from __future__ import annotations

from datetime import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.mysql import (
    BINARY,
    DATETIME,
    DECIMAL,
    INTEGER,
    SMALLINT,
    TINYINT,
    VARCHAR,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fazutil.db.fazdb.model._unique_id_model import UniqueIdModel

if TYPE_CHECKING:
    from fazutil.db.fazdb.model.guild_info import GuildInfo


class GuildHistory(UniqueIdModel):
    __tablename__ = "guild_history"

    name: Mapped[str] = mapped_column(  # stupid decision
        VARCHAR(30), ForeignKey("guild_info.name"), nullable=False, primary_key=True
    )
    level: Mapped[float] = mapped_column(DECIMAL(5, 2, unsigned=True), nullable=False)
    territories: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    wars: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    member_total: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    online_members: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False, primary_key=True)
    unique_id: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)

    guild_info: Mapped[GuildInfo] = relationship(
        "GuildInfo",
        back_populates="stat_history",
    )

    __table_args__ = (
        Index("datetime_idx", datetime.desc()),
        Index("name_idx", name),
        UniqueConstraint(unique_id, name="unique_id_idx"),
    )
