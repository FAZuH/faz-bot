from __future__ import annotations

from datetime import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BINARY, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fazutil.db.fazdb.model.base_fazdb_model import BaseFazdbModel

if TYPE_CHECKING:
    from fazutil.db.fazdb.model.guild_info import GuildInfo


class PlayerInfo(BaseFazdbModel):
    __tablename__ = "player_info"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, nullable=False)
    latest_username: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    first_join: Mapped[dt] = mapped_column(DATETIME, nullable=False)
    guild_uuid: Mapped[bytes] = mapped_column(
        BINARY(16), ForeignKey("guild_info.uuid"), default=None, nullable=True
    )

    guild: Mapped[GuildInfo | None] = relationship(
        "GuildInfo", back_populates="members", lazy="selectin"
    )
    # player_histories: Mapped[list[PlayerHistory]] = relationship(
    #     "PlayerHistory", back_populates="player_info"
    # )
