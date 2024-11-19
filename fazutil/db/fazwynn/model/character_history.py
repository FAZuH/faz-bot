from __future__ import annotations

import math
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

from fazutil.db.fazwynn.model._unique_id_model import UniqueIdModel

if TYPE_CHECKING:
    from fazutil.db.fazwynn.model.character_info import CharacterInfo


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
        Index(None, datetime.desc()),
        Index(None, character_uuid),
        UniqueConstraint(unique_id),
    )

    def get_total_level(self) -> int:
        def _sum(*args: int | float) -> int:
            ret = 0
            for arg in args:
                ret += math.floor(arg)
            return ret

        ret = _sum(
            self.level,
            self.alchemism,
            self.armouring,
            self.cooking,
            self.jeweling,
            self.scribing,
            self.tailoring,
            self.weaponsmithing,
            self.woodworking,
            self.mining,
            self.woodcutting,
            self.farming,
            self.fishing,
        )
        return ret
