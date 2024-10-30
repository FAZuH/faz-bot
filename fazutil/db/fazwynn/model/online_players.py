from sqlalchemy.dialects.mysql import BINARY, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from fazutil.db.fazwynn.model.base_fazwynn_model import BaseFazwynnModel


class OnlinePlayers(BaseFazwynnModel):
    __tablename__ = "online_players"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, nullable=False)
    server: Mapped[str] = mapped_column(VARCHAR(10), nullable=False)
