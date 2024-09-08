import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from nextcord import Interaction

from fazcord.bot.cog.wynn_track_cog import WynnTrackCog


class TestWynnTrackCog(unittest.IsolatedAsyncioTestCase):

    @staticmethod
    async def _mock_awaitable_attr() -> None: ...

    def setUp(self):
        self.bot = MagicMock()
        self.cog = WynnTrackCog(self.bot)
        self.intr = MagicMock(spec=Interaction)
        self.intr.user = MagicMock()
        self.intr.guild = MagicMock()
        self.intr.guild.id = 123456789

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._must_get_channel")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_toggle(
        self, mock_respond_successful: MagicMock, mock_must_get_channel: MagicMock
    ):
        mock_channel = MagicMock()
        mock_channel.id = "123"
        mock_channel.name = "test-channel"
        mock_must_get_channel.return_value = mock_channel
        self.bot.fazcord_db.track_entry_repository.toggle = AsyncMock(return_value=True)

        await self.cog.toggle(self.intr, "123")

        mock_must_get_channel.assert_called_once_with("123")
        self.bot.fazcord_db.track_entry_repository.toggle.assert_called_once_with("123")
        mock_respond_successful.assert_called_once_with(
            self.intr, "Toggled track entry on channel `123` (`test-channel`) to True"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_show_no_trackers(self, mock_respond_successful: MagicMock):
        self.bot.fazcord_db.track_entry_repository.select_by_guild_id = AsyncMock(
            return_value=[]
        )

        await self.cog.show(self.intr)

        self.bot.fazcord_db.track_entry_repository.select_by_guild_id.assert_called_once_with(
            123456789
        )
        mock_respond_successful.assert_called_once_with(
            self.intr, "This guild does not have any Wynn Trackers registred"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_show_with_trackers(self, mock_respond_successful: MagicMock):
        mock_entry = MagicMock()
        mock_entry.channel_id = "123"
        mock_entry.channel.channel_name = "test-channel"
        mock_entry.type = "GUILD"
        mock_entry.awaitable_attrs.channel = self._mock_awaitable_attr()
        mock_entry.awaitable_attrs.associations = self._mock_awaitable_attr()
        mock_entry.associations = [MagicMock(associated_value="test-guild")]
        self.bot.fazcord_db.track_entry_repository.select_by_guild_id = AsyncMock(
            return_value=[mock_entry]
        )

        await self.cog.show(self.intr)

        self.bot.fazcord_db.track_entry_repository.select_by_guild_id.assert_called_once_with(
            123456789
        )
        mock_respond_successful.assert_called_once_with(
            self.intr, "- `123 (test-channel)`: GUILD\n\t- `test-guild`"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._must_get_channel")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_remove(
        self, mock_respond_successful: MagicMock, mock_must_get_channel: MagicMock
    ):
        mock_channel = MagicMock()
        mock_channel.id = "123"
        mock_channel.name = "test-channel"
        mock_must_get_channel.return_value = mock_channel
        self.bot.fazcord_db.track_entry_repository.delete = AsyncMock()

        await self.cog.remove(self.intr, "123")

        mock_must_get_channel.assert_called_once_with("123")
        self.bot.fazcord_db.track_entry_repository.delete.assert_called_once_with("123")
        mock_respond_successful.assert_called_once_with(
            self.intr, "Removed track entry on channel `123` (`test-channel`)"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._add_track_entry")
    async def test_guild(self, mock_add_track_entry: MagicMock):
        await self.cog.guild(self.intr, "123", "test-guild")
        mock_add_track_entry.assert_called_once_with(
            self.intr, "123", "GUILD", "test-guild"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._add_track_entry")
    async def test_hunted(self, mock_add_track_entry: MagicMock):
        await self.cog.hunted(self.intr, "123")
        mock_add_track_entry.assert_called_once_with(self.intr, "123", "HUNTED")

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._add_track_entry")
    async def test_online(self, mock_add_track_entry: MagicMock):
        await self.cog.online(self.intr, "123", "test-user")
        mock_add_track_entry.assert_called_once_with(
            self.intr, "123", "ONLINE", "test-user"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._add_track_entry")
    async def test_player(self, mock_add_track_entry: MagicMock):
        await self.cog.player(self.intr, "123", "test-user")
        mock_add_track_entry.assert_called_once_with(
            self.intr, "123", "PLAYER", "test-user"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._add_track_entry")
    async def test_staff(self, mock_add_track_entry: MagicMock):
        await self.cog.staff(self.intr, "123")
        mock_add_track_entry.assert_called_once_with(self.intr, "123", "STAFF")

    @patch("fazcord.bot.cog.wynn_track_cog.Utils.add_to_db")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._must_get_channel")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_add_track_entry_new_entry(
        self,
        mock_respond_successful: MagicMock,
        mock_must_get_channel: MagicMock,
        mock_add_to_db: MagicMock,
    ):
        mock_channel = MagicMock()
        mock_channel.id = "123"
        mock_channel.name = "test-channel"
        mock_must_get_channel.return_value = mock_channel
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id = AsyncMock(
            return_value=None
        )
        self.bot.fazcord_db.track_entry_repository.model = MagicMock()
        self.bot.fazcord_db.track_entry_repository.insert = AsyncMock()

        await self.cog._add_track_entry(self.intr, "123", "GUILD", "test-guild")

        mock_must_get_channel.assert_called_once_with("123")
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id.assert_called_once_with(
            "123",
            session=self.bot.fazcord_db.enter_async_session.return_value.__aenter__.return_value,
        )
        self.bot.fazcord_db.track_entry_repository.insert.assert_called_once()
        mock_respond_successful.assert_called_once_with(
            self.intr, "Added `GUILD` track entry on channel `123` (`test-channel`)"
        )

    @patch("fazcord.bot.cog.wynn_track_cog.Utils.add_to_db")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._must_get_channel")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_add_track_entry_existing_entry(
        self,
        mock_respond_successful: MagicMock,
        mock_must_get_channel: MagicMock,
        mock_add_to_db: MagicMock,
    ):
        mock_channel = MagicMock()
        mock_channel.id = "123"
        mock_channel.name = "test-channel"
        mock_must_get_channel.return_value = mock_channel
        mock_track_entry = MagicMock()
        mock_track_entry.associations = []
        mock_track_entry.awaitable_attrs.associations = self._mock_awaitable_attr()
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id = AsyncMock(
            return_value=mock_track_entry
        )
        self.bot.fazcord_db.track_entry_association_repository.model = MagicMock()
        self.bot.fazcord_db.track_entry_association_repository.insert = AsyncMock()
        self.bot.fazdb_db.guild_info_repository.get_guild = AsyncMock(
            return_value=MagicMock(uuid="test-uuid")
        )

        await self.cog._add_track_entry(self.intr, "123", "GUILD", "test-guild")

        mock_must_get_channel.assert_called_once_with("123")
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id.assert_called_once_with(
            "123",
            session=self.bot.fazcord_db.enter_async_session.return_value.__aenter__.return_value,
        )
        self.bot.fazcord_db.track_entry_association_repository.insert.assert_called_once()
        mock_respond_successful.assert_called_once_with(
            self.intr,
            "Added guild `test-guild` to `GUILD` track entry on channel `123` (`test-channel`)",
        )

    @patch("fazcord.bot.cog.wynn_track_cog.Utils.add_to_db")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._must_get_channel")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_add_track_entry_remove_existing_value(
        self,
        mock_respond_successful: MagicMock,
        mock_must_get_channel: MagicMock,
        mock_add_to_db: MagicMock,
    ):
        mock_channel = MagicMock()
        mock_channel.id = "123"
        mock_channel.name = "test-channel"
        mock_must_get_channel.return_value = mock_channel
        mock_track_entry = MagicMock()
        mock_track_entry.associations = [
            MagicMock(associated_value="test-uuid"),
            MagicMock(associated_value="test-uuid"),
        ]
        mock_track_entry.awaitable_attrs.associations = self._mock_awaitable_attr()
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id = AsyncMock(
            return_value=mock_track_entry
        )
        self.bot.fazcord_db.track_entry_association_repository.model = MagicMock()
        self.bot.fazcord_db.track_entry_association_repository.insert = AsyncMock()
        self.bot.fazdb_db.guild_info_repository.get_guild = AsyncMock(
            return_value=MagicMock(uuid="test-uuid")
        )

        await self.cog._add_track_entry(self.intr, "123", "GUILD", "test-guild")

        mock_must_get_channel.assert_called_once_with("123")
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id.assert_called_once_with(
            "123",
            session=self.bot.fazcord_db.enter_async_session.return_value.__aenter__.return_value,
        )
        mock_respond_successful.assert_called_once_with(
            self.intr,
            "Removed guild `test-guild` from `GUILD` track entry on channel `123` (`test-channel`)",
        )

    @patch("fazcord.bot.cog.wynn_track_cog.Utils.add_to_db")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._must_get_channel")
    @patch("fazcord.bot.cog.wynn_track_cog.WynnTrackCog._respond_successful")
    async def test_add_track_entry_remove_last_value(
        self,
        mock_respond_successful: MagicMock,
        mock_must_get_channel: MagicMock,
        mock_add_to_db: MagicMock,
    ):
        mock_channel = MagicMock()
        mock_channel.id = "123"
        mock_channel.name = "test-channel"
        mock_must_get_channel.return_value = mock_channel
        mock_track_entry = MagicMock()
        mock_track_entry.associations = [MagicMock(associated_value="test-uuid")]
        mock_track_entry.awaitable_attrs.associations = self._mock_awaitable_attr()
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id = AsyncMock(
            return_value=mock_track_entry
        )
        self.bot.fazcord_db.track_entry_association_repository.model = MagicMock()
        self.bot.fazcord_db.track_entry_association_repository.insert = AsyncMock()
        self.bot.fazdb_db.guild_info_repository.get_guild = AsyncMock(
            return_value=MagicMock(uuid="test-uuid")
        )

        await self.cog._add_track_entry(self.intr, "123", "GUILD", "test-guild")

        mock_must_get_channel.assert_called_once_with("123")
        self.bot.fazcord_db.track_entry_repository.select_by_channel_id.assert_called_once_with(
            "123",
            session=self.bot.fazcord_db.enter_async_session.return_value.__aenter__.return_value,
        )
        mock_respond_successful.assert_called_once_with(
            self.intr, "Removed track entry on channel `123` (`test-channel`)"
        )
