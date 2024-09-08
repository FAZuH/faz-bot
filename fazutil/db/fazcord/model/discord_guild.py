from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fazutil.db.fazcord.model.base_fazcord_model import BaseFazcordModel

if TYPE_CHECKING:
    from fazutil.db.fazcord.model.discord_channel import DiscordChannel


class DiscordGuild(BaseFazcordModel):
    __tablename__ = "discord_guild"

    guild_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    guild_name: Mapped[str] = mapped_column(VARCHAR(36), nullable=False)

    channels: Mapped[list[DiscordChannel]] = relationship(
        "DiscordChannel", back_populates="discord_guild", lazy="selectin"
    )
