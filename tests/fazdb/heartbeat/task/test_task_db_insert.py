from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from fazdb.heartbeat.task.task_db_insert import TaskDbInsert
from fazutil.api.wynn.response.guild_response import GuildResponse
from fazutil.api.wynn.response.online_players_response import OnlinePlayersResponse
from fazutil.api.wynn.response.player_response import PlayerResponse


class TestTaskDbInsert(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self._adapter_patcher = patch(
            "fazdb.heartbeat.task.task_db_insert.ApiResponseAdapter"
        )
        mock_adapter_class = self._adapter_patcher.start()
        self._mock_adapter = mock_adapter_class.return_value
        self._mock_api = AsyncMock()
        self._mock_db = AsyncMock()
        self._mock_request_list = MagicMock()
        self._mock_response_list = MagicMock()
        self._task_db_insert = TaskDbInsert(
            self._mock_api,
            self._mock_db,
            self._mock_request_list,
            self._mock_response_list,
        )

    def test_setup(self) -> None:
        # Prepare
        self._mock_db.create_all = AsyncMock()
        # Act
        self._task_db_insert.setup()
        # Assert
        self._mock_db.create_all.assert_called_once()

    def test_run_insert_fazdb_uptime(self) -> None:
        # Prepare
        model = self._mock_db.fazdb_uptime_repository.model = Mock()
        with patch("fazdb.heartbeat.task.task_db_insert.datetime") as mock_datetime:
            # Act
            self._task_db_insert.run()
            # Assert
            model.assert_called_once_with(
                start_time=self._task_db_insert._start_time,
                stop_time=mock_datetime.now.return_value,
            )
            self._mock_db.fazdb_uptime_repository.insert.assert_awaited_once_with(
                model.return_value, replace_on_duplicate=True
            )

    def test_run_empty_response_list(self) -> None:
        # Prepare
        self._task_db_insert._run = AsyncMock()
        self._mock_response_list.get.return_value = None
        self._task_db_insert._response_handler = handler = Mock()
        # Act
        self._task_db_insert.run()
        # Assert
        self._task_db_insert._run.assert_called_once()
        handler.handle_onlineplayers_response.assert_not_called()
        handler.handle_player_response.assert_not_called()
        handler.handle_guild_response.assert_not_called()

    def test_run_non_empty_response_list(self) -> None:
        # Prepare
        online_players = Mock(spec_set=OnlinePlayersResponse)
        player = Mock(spec_set=PlayerResponse)
        guild = Mock(spec_set=GuildResponse)
        self._task_db_insert._response_handler = handler = Mock()
        self._mock_response_list.get.return_value = [online_players, player, guild]
        # Act
        self._task_db_insert.run()
        # Assert
        handler.handle_onlineplayers_response.assert_called_once_with(online_players)
        handler.handle_player_response.assert_called_once_with([player])
        handler.handle_guild_response.assert_called_once_with([guild])

    async def test_insert_online_players_response(self) -> None:
        # Prepare
        adapter = self._mock_adapter.OnlinePlayers
        db = self._mock_db
        # Act
        await self._task_db_insert._insert_online_players_response(Mock())
        # Assert
        db.online_players_repository.update.assert_awaited_once_with(
            adapter.to_online_players.return_value
        )
        db.player_activity_history_repository.insert.assert_awaited_once_with(
            adapter.to_player_activity_history.return_value, replace_on_duplicate=True
        )
        db.worlds_repository.update_worlds.assert_awaited_once_with(
            list(adapter.to_worlds.return_value)
        )

    async def test_insert_player_responses(self) -> None:
        # Prepare
        a = self._mock_adapter.Player
        a.to_player_info.return_value = player_info = Mock()
        a.to_character_info.return_value = character_info = [Mock()]
        a.to_player_history.return_value = player_history = Mock()
        a.to_character_history.return_value = character_history = [Mock()]
        db = self._mock_db
        # Act
        await self._task_db_insert._insert_player_responses([Mock()])
        # Assert
        db.player_info_repository.safe_insert.assert_awaited_once_with(
            [player_info], replace_on_duplicate=True
        )
        db.character_info_repository.insert.assert_awaited_once_with(
            character_info, replace_on_duplicate=True
        )
        db.player_history_repository.insert.assert_awaited_once_with(
            [player_history], ignore_on_duplicate=True
        )
        db.character_history_repository.insert.assert_awaited_once_with(
            character_history, ignore_on_duplicate=True
        )

    async def test_insert_guild_response(self) -> None:
        # Prepare
        a = self._mock_adapter.Guild
        a.to_guild_member_history.return_value = guild_member_history = [Mock()]
        db = self._mock_db
        # Act
        await self._task_db_insert._insert_guild_response([Mock()])
        # Assert
        db.guild_info_repository.insert.assert_awaited_once_with(
            [a.to_guild_info.return_value], replace_on_duplicate=True
        )
        db.guild_history_repository.insert.assert_awaited_once_with(
            [a.to_guild_history.return_value], ignore_on_duplicate=True
        )
        db.guild_member_history_repository.insert.assert_awaited_once_with(
            guild_member_history, ignore_on_duplicate=True
        )

    def tearDown(self) -> None:
        self._adapter_patcher.stop()
