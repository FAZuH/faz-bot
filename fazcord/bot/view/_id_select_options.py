from enum import Enum


class IdSelectOptions(Enum):
    """Mapping of enum member to display value for IdSelect."""

    ALL = "All"

    # Categorical
    USERNAME = "Username"
    GUILD = "Guild"  # Guild name and rank

    # Numerical
    PLAYTIME = "Playtime"
    LEVEL = "Level"  # level + (xp_percentage / 100
    MOBS_KILLED = "Mobs Killed"
    CHESTS_FOUND = "Chests Found"
    LOGINS = "Logins"
    DEATHS = "Deaths"
    DISCOVERIES = "Discoveries"
    PROFESSIONS = "Professions"
    DUNGEON_COMPLETIONS = "Dungeon Completions"
    QUEST_COMPLETIONS = "Quest Completions"
    RAID_COMPLETIONS = "Raid Completions"
