from __future__ import annotations

from enum import Enum


class IdSelectOptionsType(Enum):
    CATEGORICAL = "Categorical"
    NUMERICAL = "Numerical"
    ALL = "ALL"


class _IdSelectOptionsMember:
    def __init__(self, value: str, type: IdSelectOptionsType) -> None:
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


class IdSelectOptions(Enum):
    """Mapping of enum member to display value for IdSelect."""

    ALL = _IdSelectOptionsMember("All", IdSelectOptionsType.ALL)

    GUILD = _IdSelectOptionsMember("Guild", IdSelectOptionsType.CATEGORICAL)
    USERNAME = _IdSelectOptionsMember("Username", IdSelectOptionsType.CATEGORICAL)

    LEVEL = _IdSelectOptionsMember("Level", IdSelectOptionsType.NUMERICAL)
    """level + (xp/100)"""
    WARS = _IdSelectOptionsMember("Wars", IdSelectOptionsType.NUMERICAL)
    """wars"""
    PLAYTIME = _IdSelectOptionsMember("Playtime", IdSelectOptionsType.NUMERICAL)
    """playtime"""
    MOBS_KILLED = _IdSelectOptionsMember("Mobs Killed", IdSelectOptionsType.NUMERICAL)
    """mobs_killed"""
    CHESTS_FOUND = _IdSelectOptionsMember("Chests Found", IdSelectOptionsType.NUMERICAL)
    """chests_found"""
    LOGINS = _IdSelectOptionsMember("Logins", IdSelectOptionsType.NUMERICAL)
    """logins"""
    DEATHS = _IdSelectOptionsMember("Deaths", IdSelectOptionsType.NUMERICAL)
    """deaths"""
    CHALLENGES = _IdSelectOptionsMember("Challenges", IdSelectOptionsType.NUMERICAL)
    """hardcord, ultimate_ironman, ironman, craftsman, hunted"""
    PROFESSIONS = _IdSelectOptionsMember("Professions", IdSelectOptionsType.NUMERICAL)
    """alchemism, armouring, cooking, jeweling, scribing, tailoring, weaponsmithing, woodworking, mining, woodcutting, farming, fishing"""
    COMPLETIONS = _IdSelectOptionsMember("Completions", IdSelectOptionsType.NUMERICAL)
    """dungeon_completions, quest_completions, raid_completions"""

    @property
    def type(self) -> IdSelectOptionsType:
        return self.value.type
