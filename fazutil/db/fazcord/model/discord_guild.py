from typing import Any

from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from fazutil.db.fazcord.model.base_fazcord_model import BaseFazcordModel


class DiscordGuild(BaseFazcordModel):
    __tablename__ = "discord_guild"

    guild_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    guild_name: Mapped[str] = mapped_column(VARCHAR(36), nullable=False)

    def __init__(self, *, guild_id: int, guild_name: str, **kw: Any) -> None:
        self.guild_id = guild_id
        self.guild_name = guild_name
        super().__init__(**kw)
