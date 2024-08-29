from __future__ import annotations

from datetime import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy.dialects.mysql import BINARY, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fazutil.db.fazdb.model.base_fazdb_model import BaseFazdbModel

if TYPE_CHECKING:
    from fazutil.db.fazdb.model.player_info import PlayerInfo


class GuildInfo(BaseFazdbModel):
    __tablename__ = "guild_info"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    prefix: Mapped[str] = mapped_column(VARCHAR(4), nullable=False)
    created: Mapped[dt] = mapped_column(DATETIME, nullable=False)

    members: Mapped[list[PlayerInfo]] = relationship(
        "PlayerInfo",
        back_populates="guild",
        foreign_keys="PlayerInfo.guild_uuid",
        lazy="selectin",
    )
