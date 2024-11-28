from __future__ import annotations

from enum import Enum


class PlayerHistoryIdOptionsType(Enum):
    CATEGORICAL = "Categorical"
    NUMERICAL = "Numerical"
    ALL = "ALL"


class _IdOptionsMember:
    def __init__(self, value: str, type: PlayerHistoryIdOptionsType) -> None:
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


class PlayerHistoryIdOptions(Enum):
    """Mapping of enum member to display value for IdSelect."""

    ALL = _IdOptionsMember("All", PlayerHistoryIdOptionsType.ALL)

    GUILD = _IdOptionsMember("Guild", PlayerHistoryIdOptionsType.CATEGORICAL)
    USERNAME = _IdOptionsMember("Username", PlayerHistoryIdOptionsType.CATEGORICAL)

    LEVEL = _IdOptionsMember("Level", PlayerHistoryIdOptionsType.NUMERICAL)
    """level + (xp/100)"""
    WARS = _IdOptionsMember("Wars", PlayerHistoryIdOptionsType.NUMERICAL)
    """wars"""
    PLAYTIME = _IdOptionsMember("Playtime", PlayerHistoryIdOptionsType.NUMERICAL)
    """playtime"""
    MOBS_KILLED = _IdOptionsMember("Mobs Killed", PlayerHistoryIdOptionsType.NUMERICAL)
    """mobs_killed"""
    CHESTS_FOUND = _IdOptionsMember("Chests Found", PlayerHistoryIdOptionsType.NUMERICAL)
    """chests_found"""
    LOGINS = _IdOptionsMember("Logins", PlayerHistoryIdOptionsType.NUMERICAL)
    """logins"""
    DEATHS = _IdOptionsMember("Deaths", PlayerHistoryIdOptionsType.NUMERICAL)
    """deaths"""
    CHALLENGES = _IdOptionsMember("Challenges", PlayerHistoryIdOptionsType.NUMERICAL)
    """hardcord, ultimate_ironman, ironman, craftsman, hunted"""
    PROFESSIONS = _IdOptionsMember("Professions", PlayerHistoryIdOptionsType.NUMERICAL)
    """alchemism, armouring, cooking, jeweling, scribing, tailoring, weaponsmithing, woodworking, mining, woodcutting, farming, fishing"""
    COMPLETIONS = _IdOptionsMember("Completions", PlayerHistoryIdOptionsType.NUMERICAL)
    """dungeon_completions, quest_completions, raid_completions"""

    @property
    def type(self) -> PlayerHistoryIdOptionsType:
        return self.value.type
