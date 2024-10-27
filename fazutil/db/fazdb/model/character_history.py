from __future__ import annotations

from datetime import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.mysql import (
    BIGINT,
    BINARY,
    BOOLEAN,
    DATETIME,
    DECIMAL,
    INTEGER,
    TINYINT,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fazutil.db.fazdb.model._unique_id_model import UniqueIdModel

if TYPE_CHECKING:
    from fazutil.db.fazdb.model.character_info import CharacterInfo


class CharacterHistory(UniqueIdModel):
    """
    Assumptions:
        - There must be a CharacterInfo entry for each CharacterHistory entry
    """

    __tablename__ = "character_history"

    character_uuid: Mapped[bytes] = mapped_column(
        BINARY(16),
        ForeignKey("character_info.character_uuid"),
        nullable=False,
        primary_key=True,
    )
    level: Mapped[int] = mapped_column(TINYINT, nullable=False)
    xp: Mapped[int] = mapped_column(BIGINT, nullable=False)
    wars: Mapped[int] = mapped_column(INTEGER, nullable=False)
    playtime: Mapped[float] = mapped_column(DECIMAL(7, 2), nullable=False)
    mobs_killed: Mapped[int] = mapped_column(INTEGER, nullable=False)
    chests_found: Mapped[int] = mapped_column(INTEGER, nullable=False)
    logins: Mapped[int] = mapped_column(INTEGER, nullable=False)
    deaths: Mapped[int] = mapped_column(INTEGER, nullable=False)
    discoveries: Mapped[int] = mapped_column(INTEGER, nullable=False)
    hardcore: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    ultimate_ironman: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    ironman: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    craftsman: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    hunted: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    alchemism: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    armouring: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    cooking: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    jeweling: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    scribing: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    tailoring: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    weaponsmithing: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    woodworking: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    mining: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    woodcutting: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    farming: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    fishing: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    dungeon_completions: Mapped[int] = mapped_column(INTEGER, nullable=False)
    quest_completions: Mapped[int] = mapped_column(INTEGER, nullable=False)
    raid_completions: Mapped[int] = mapped_column(INTEGER, nullable=False)
    datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False, primary_key=True)
    unique_id: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)

    character_info: Mapped[CharacterInfo] = relationship(
        "CharacterInfo",
        back_populates="stat_history",
    )

    __table_args__ = (
        Index("datetime_idx", datetime.desc()),
        Index("character_uuid_idx", character_uuid),
        UniqueConstraint(unique_id, name="unique_id_idx"),
    )
