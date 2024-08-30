from typing import Any

from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from fazutil.db.fazcord.model.base_fazcord_model import BaseFazcordModel


class DiscordUser(BaseFazcordModel):
    __tablename__ = "discord_user"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(36), nullable=False)

    def __init__(self, *, user_id: int, username: str, **kw: Any) -> None:
        self.user_id = user_id
        self.username = username
        super().__init__(**kw)
