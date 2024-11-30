from __future__ import annotations

from enum import Enum


class PlayerHistoryDataOptionsType(Enum):
    CATEGORICAL = "Categorical"
    NUMERICAL = "Numerical"
    ALL = "ALL"


class _IdOptionsMember:
    def __init__(self, value: str, type: PlayerHistoryDataOptionsType) -> None:
        self._type = type
        self._value = value

    @property
    def type(self):
        """The type property."""
        return self._type

    @property
    def value(self):
        """The value property."""
        return self._value


class PlayerHistoryDataOptions(Enum):
    """Mapping of enum member to display value for IdSelect."""

    ALL = _IdOptionsMember("All", PlayerHistoryDataOptionsType.ALL)

    GUILD = _IdOptionsMember("Guild", PlayerHistoryDataOptionsType.CATEGORICAL)
    USERNAME = _IdOptionsMember("Username", PlayerHistoryDataOptionsType.CATEGORICAL)

    LEVEL = _IdOptionsMember("Level", PlayerHistoryDataOptionsType.NUMERICAL)
    """level + (xp/100)"""
    WARS = _IdOptionsMember("Wars", PlayerHistoryDataOptionsType.NUMERICAL)
    """wars"""
    PLAYTIME = _IdOptionsMember("Playtime", PlayerHistoryDataOptionsType.NUMERICAL)
    """playtime"""
    MOBS_KILLED = _IdOptionsMember("Mobs Killed", PlayerHistoryDataOptionsType.NUMERICAL)
    """mobs_killed"""
    CHESTS_FOUND = _IdOptionsMember("Chests Found", PlayerHistoryDataOptionsType.NUMERICAL)
    """chests_found"""
    LOGINS = _IdOptionsMember("Logins", PlayerHistoryDataOptionsType.NUMERICAL)
    """logins"""
    DEATHS = _IdOptionsMember("Deaths", PlayerHistoryDataOptionsType.NUMERICAL)
    """deaths"""
    CHALLENGES = _IdOptionsMember("Challenges", PlayerHistoryDataOptionsType.NUMERICAL)
    """hardcord, ultimate_ironman, ironman, craftsman, hunted"""
    PROFESSIONS = _IdOptionsMember("Professions", PlayerHistoryDataOptionsType.NUMERICAL)
    """alchemism, armouring, cooking, jeweling, scribing, tailoring, weaponsmithing, woodworking, mining, woodcutting, farming, fishing"""
    COMPLETIONS = _IdOptionsMember("Completions", PlayerHistoryDataOptionsType.NUMERICAL)
    """dungeon_completions, quest_completions, raid_completions"""

    @property
    def type(self) -> PlayerHistoryDataOptionsType:
        return self.value.type
