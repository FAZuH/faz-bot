import asyncio
import json

from loguru import logger

from fazutil.api.wynn.response.guild_response import GuildResponse
from fazutil.api.wynn.response.online_players_response import OnlinePlayersResponse
from fazutil.api.wynn.response.player_response import PlayerResponse
from fazutil.api.wynn.wynn_api import WynnApi


class FixturesApiCreator:
    _ONLINE_PLAYERS_FIXTURE_FP = "tests/_fixtures/online_players.json"
    _PLAYERS_FIXTURE_FP = "tests/_fixtures/players.json"
    _GUILDS_FIXTURE_FP = "tests/_fixtures/guilds.json"

    def __init__(self) -> None:
        self._api = WynnApi()

    async def create_fixtures_data(self) -> None:
        await self._api.start()
        logger.info("Creating fixture data...")

        uuids = await self._api.player.get_online_uuids()
        assert uuids
        with open(self._ONLINE_PLAYERS_FIXTURE_FP, "w") as f:
            json.dump({0: [uuids.body.raw, uuids.headers.raw]}, f, indent=4)
        logger.info(f"Saved fixture (file: {self._ONLINE_PLAYERS_FIXTURE_FP})")

        players = await self._get_online_player_stats(uuids)
        logger.info(f"Fetched stats for {len(players)} players.")
        to_dump1 = {
            i: [resp.body.raw, resp.headers.raw] for i, resp in enumerate(players)
        }
        with open(self._PLAYERS_FIXTURE_FP, "w") as f:
            json.dump(to_dump1, f, indent=4)
        logger.info(f"Saved fixture (file: {self._PLAYERS_FIXTURE_FP})")

        guilds = await self._get_online_guild_stats(players)
        logger.info(f"Fetched stats for {len(guilds)} guilds.")
        to_dump2 = {
            i: [resp.body.raw, resp.headers.raw] for i, resp in enumerate(guilds)
        }
        with open(self._GUILDS_FIXTURE_FP, "w") as f:
            json.dump(to_dump2, f, indent=4)
        logger.info(f"Saved fixture (file: {self._GUILDS_FIXTURE_FP})")

        logger.success("Fixture data creation completed.")
        await self._api.close()

    async def _get_online_player_stats(
        self, online_uuids: OnlinePlayersResponse
    ) -> list[PlayerResponse]:
        ret: list[PlayerResponse] = []
        concurr_reqs = 25
        uuids = list((online_uuids).body.players)
        total = len(uuids)
        logger.info(f"Starting to fetch player stats for {total} players...")
        while uuids:
            curr_req = uuids[:concurr_reqs]
            uuids = uuids[concurr_reqs:]
            responses = await asyncio.gather(
                *[
                    self._api.player.get_full_stats(uuid.username_or_uuid)
                    for uuid in curr_req
                ]
            )
            ret.extend(responses)
            progress = 100 * (total - len(uuids)) / total
            logger.info(
                f"Fetched stats for {len(ret)} players ({progress:.2f}% complete)."
            )
        return ret

    async def _get_online_guild_stats(
        self, online_players: list[PlayerResponse]
    ) -> list[GuildResponse]:
        ret: list[GuildResponse] = []
        concurr_reqs = 25
        players = online_players
        guilds: set[str] = set()
        for resp in players:
            if resp.body.guild:
                guilds.add(resp.body.guild.name)
        guild_names = list(guilds)
        total = len(guild_names)
        logger.info(f"Starting to fetch guild stats for {total} guilds...")
        while guild_names:
            curr_req = guild_names[:concurr_reqs]
            guild_names = guild_names[concurr_reqs:]
            responses = await asyncio.gather(
                *[self._api.guild.get(name) for name in curr_req]
            )
            ret.extend(responses)
            progress = 100 * (total - len(guild_names)) / total
            logger.info(
                f"Fetched stats for {len(ret)} guilds ({progress:.2f}% complete)."
            )
        return ret
