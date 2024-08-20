import json
import os

from fazutil.api.wynn.response import (
    GuildResponse,
    OnlinePlayersResponse,
    PlayerResponse,
)


class FixturesApi:

    _ONLINE_PLAYERS_FIXTURE_FP = "tests/_fixtures/online_players.json"
    _PLAYERS_FIXTURE_FP = "tests/_fixtures/players.json"
    _GUILDS_FIXTURE_FP = "tests/_fixtures/guilds.json"

    online_uuids: OnlinePlayersResponse | None = None
    player_stats: list[PlayerResponse] = []
    guild_stats: list[GuildResponse] = []

    @classmethod
    def load_fixtures(cls) -> None:
        cls._load_online_uuids()
        cls._load_players()
        cls._load_guilds()

    @classmethod
    def _load_online_uuids(cls) -> None:
        if os.path.exists(cls._ONLINE_PLAYERS_FIXTURE_FP):
            with open(cls._ONLINE_PLAYERS_FIXTURE_FP, "r") as f:
                cls.online_uuids = OnlinePlayersResponse(*(json.load(f)["0"]))
        if cls.online_uuids is None:
            raise ValueError("No online players fixture found")

    @classmethod
    def _load_players(cls) -> None:
        if os.path.exists(cls._PLAYERS_FIXTURE_FP):
            with open(cls._PLAYERS_FIXTURE_FP, "r") as f:
                cls.player_stats = [
                    PlayerResponse(*resp) for resp in json.load(f).values()
                ]
        if cls.player_stats is None:
            raise ValueError("No player stats fixture found")

    @classmethod
    def _load_guilds(cls) -> None:
        if os.path.exists(cls._GUILDS_FIXTURE_FP):
            with open(cls._GUILDS_FIXTURE_FP, "r") as f:
                cls.guild_stats = [
                    GuildResponse(*resp) for resp in json.load(f).values()
                ]
        if cls.guild_stats is None:
            raise ValueError("No guild stats fixture found")
