from datetime import datetime, timedelta
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, create_autospec, patch

from nextcord import Color, Interaction
from sortedcontainers.sortedlist import Sequence

from fazcord.bot.view.guild_activity_view import GuildActivityView


class TestGuildActivityView(IsolatedAsyncioTestCase):

    @staticmethod
    async def _mock_awaitable_attr() -> None: ...

    @patch("fazcord.bot.view.guild_activity_view.PaginationEmbed")
    async def test_run_not_empty(self, mock_embed: MagicMock) -> None:
        # Prepare
        mock_bot = MagicMock()
        mock_interaction = create_autospec(Interaction, spec_set=True)

        mock_guild_info = MagicMock()
        mock_guild_info.members = self._get_mock_player_infos()
        mock_guild_info.name = "MockGuild"
        mock_guild_info.awaitable_attrs.members = self._mock_awaitable_attr()

        mock_repo = (
            mock_bot.fazdb_db.player_activity_history_repository.get_activities_between_period
        ) = AsyncMock()
        mock_repo.side_effect = self._get_mock_player_activity()

        embed_ins = mock_embed.return_value.get_base.return_value

        view = GuildActivityView(
            mock_bot,
            mock_interaction,
            mock_guild_info,
            datetime.fromtimestamp(100),
            datetime.fromtimestamp(300),
        )

        embed_ins.get_items.return_value = view._activity_res

        # Act
        await view.run()

        # Assert
        self.maxDiff = 2000
        mock_embed.assert_called_once_with(
            mock_interaction,
            view._activity_res,
            title="Guild Members Activity",
            color=Color.teal(),
        )
        self.assertMultiLineEqual(
            embed_ins.description,
            "`Guild  : `MockGuild\n"
            "`Period : `<t:100:R> to <t:300:R>\n"
            "```ml\n"
            "|   No | Username   | Activity   |\n"
            "|------|------------|------------|\n"
            "|    1 | e          | 3m         |\n"
            "|    2 | d          | 3m         |\n"
            "|    3 | c          | 3m         |\n"
            "|    4 | b          | 3m         |\n"
            "|    5 | a          | 3m         |\n```",
        )
        mock_interaction.send.assert_awaited_once_with(embed=embed_ins, view=view)

    @staticmethod
    def _get_mock_player_infos() -> Sequence[MagicMock]:
        return [MagicMock(latest_username=letter) for letter in "abcde"]

    @staticmethod
    def _get_mock_player_activity() -> Sequence[Sequence[MagicMock]]:
        ret = []
        getts = lambda x: datetime.fromtimestamp(x)
        ret.append([MagicMock(logon_datetime=getts(50), logoff_datetime=getts(350))])
        ret.append([MagicMock(logon_datetime=getts(50), logoff_datetime=getts(350))])
        ret.append([MagicMock(logon_datetime=getts(50), logoff_datetime=getts(350))])
        ret.append([MagicMock(logon_datetime=getts(50), logoff_datetime=getts(350))])
        ret.append([MagicMock(logon_datetime=getts(50), logoff_datetime=getts(350))])
        return ret
