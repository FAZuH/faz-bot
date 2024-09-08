from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DATETIME, INTEGER, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fazutil.db.fazcord.model.base_fazcord_model import BaseFazcordModel

if TYPE_CHECKING:
    from fazutil.db.fazcord.model.discord_channel import DiscordChannel
    from fazutil.db.fazcord.model.discord_user import DiscordUser
    from fazutil.db.fazcord.model.track_entry_associations import TrackEntryAssociation


class TrackEntry(BaseFazcordModel):
    __tablename__ = "track_entry"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    channel_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("discord_channel.channel_id")
    )
    created_by: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("discord_user.user_id", ondelete="CASCADE")
    )
    created_on: Mapped[datetime] = mapped_column(DATETIME, server_default=func.now())
    type: Mapped[str] = mapped_column(
        ENUM("GUILD", "HUNTED", "ONLINE", "PLAYER", "STAFF"), nullable=False
    )

    creator: Mapped[DiscordUser] = relationship(
        "DiscordUser", back_populates="track_entries", lazy="selectin"
    )
    channel: Mapped[DiscordChannel] = relationship(
        "DiscordChannel", back_populates="track_entry", lazy="selectin", uselist=False
    )
    associations: Mapped[list[TrackEntryAssociation]] = relationship(
        "TrackEntryAssociation",
        back_populates="track_entry",
        cascade="all, delete-orphan",
    )
