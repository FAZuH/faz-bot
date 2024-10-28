from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING

from loguru import logger

from fazbeat.api_collect.task._response_handler import ResponseHandler
from fazbeat.api_collect.task.api_response_adapter import ApiResponseAdapter
from fazutil.api.wynn.response.guild_response import GuildResponse
from fazutil.api.wynn.response.online_players_response import OnlinePlayersResponse
from fazutil.api.wynn.response.player_response import PlayerResponse
from fazutil.heartbeat.task.itask import ITask

if TYPE_CHECKING:
    from fazbeat.api_collect.task.request_queue import RequestQueue
    from fazbeat.api_collect.task.response_queue import ResponseQueue
    from fazutil.api.wynn.wynn_api import WynnApi
    from fazutil.db.fazdb.fazdb_database import FazdbDatabase


class TaskDbInsert(ITask):
    """Inserts API responses to database."""

    def __init__(
        self,
        api: WynnApi,
        db: FazdbDatabase,
        request_list: RequestQueue,
        response_list: ResponseQueue,
    ) -> None:
        self._api = api
        self._db = db
        self._request_list = request_list
        self._response_list = response_list

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = datetime.now()
        self._response_adapter = ApiResponseAdapter()
        self._response_handler = ResponseHandler(self._api, self._request_list)
        self._start_time = datetime.now()

    def teardown(self) -> None: ...

    def run(self) -> None:
        with logger.catch(level="ERROR"):
            self._event_loop.run_until_complete(self._run())
        self._latest_run = datetime.now()

    async def _run(self) -> None:
        model = self._db.fazdb_uptime.model
        await self._db.fazdb_uptime.insert(
            model(start_time=self._start_time, stop_time=datetime.now()),
            replace_on_duplicate=True,
        )

        online_players_resp: None | OnlinePlayersResponse = None
        player_resps: list[PlayerResponse] = []
        guild_resps: list[GuildResponse] = []
        for resp in self._response_list.get():
            if isinstance(resp, PlayerResponse):
                player_resps.append(resp)
            elif isinstance(resp, OnlinePlayersResponse):
                online_players_resp = resp
            elif isinstance(resp, GuildResponse):
                guild_resps.append(resp)

        # NOTE: Make sure responses are handled first before inserting.
        # NOTE: Insert online players requires the most recent response_handler.online_players data.
        self._response_handler.handle_onlineplayers_response(online_players_resp)
        self._response_handler.handle_player_response(player_resps)
        self._response_handler.handle_guild_response(guild_resps)

        await self._insert_online_players_response(online_players_resp)
        await self._insert_guild_response(guild_resps)
        await self._insert_player_responses(player_resps)

    async def _insert_online_players_response(
        self, resp: OnlinePlayersResponse | None
    ) -> None:
        if not resp or not resp.body.raw:
            return
        adapter = self._response_adapter.OnlinePlayers

        online_players = adapter.to_online_players(resp)
        player_activity_history = adapter.to_player_activity_history(
            resp, self._response_handler.online_players
        )
        worlds = list(adapter.to_worlds(resp))

        db = self._db
        await db.online_players.update(online_players)
        await db.player_activity_history.insert(
            player_activity_history, replace_on_duplicate=True
        )
        await db.worlds.update_worlds(worlds)

    async def _insert_player_responses(self, resps: list[PlayerResponse]) -> None:
        if not resps:
            return

        adapter = self._response_adapter.Player
        character_history = []
        character_info = []
        player_history = []
        player_info = []
        for resp in resps:
            character_history.extend(adapter.to_character_history(resp))
            character_info.extend(adapter.to_character_info(resp))
            player_history.append(adapter.to_player_history(resp))
            player_info.append(adapter.to_player_info(resp))

        db = self._db
        await db.player_info.safe_insert(player_info, replace_on_duplicate=True)
        await db.character_info.insert(character_info, replace_on_duplicate=True)
        await db.player_history.insert(player_history, ignore_on_duplicate=True)
        await db.character_history.insert(character_history, ignore_on_duplicate=True)

    async def _insert_guild_response(self, resps: list[GuildResponse]) -> None:
        if not resps:
            return

        adapter = self._response_adapter.Guild
        guild_info = []
        guild_history = []
        guild_member_history = []
        for resp in resps:
            guild_info.append(adapter.to_guild_info(resp))
            guild_history.append(adapter.to_guild_history(resp))
            guild_member_history.extend(adapter.to_guild_member_history(resp))

        db = self._db
        await db.guild_info.insert(guild_info, replace_on_duplicate=True)
        await db.guild_history.insert(guild_history, ignore_on_duplicate=True)
        await db.guild_member_history.insert(
            guild_member_history, ignore_on_duplicate=True
        )

    @property
    def response_handler(self) -> ResponseHandler:
        return self._response_handler

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def latest_run(self) -> datetime:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__
