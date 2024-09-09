from datetime import datetime, timedelta
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, create_autospec, patch

from nextcord import Color, Interaction

from fazcord.bot.view.activity_view import ActivityView


class TestActivityView(IsolatedAsyncioTestCase):
    @patch("fazcord.bot.view.activity_view.CustomEmbed")
    async def test_run(self, mock_embed: MagicMock) -> None:
        # Prepare
        mock_bot = MagicMock()
        mock_interaction = create_autospec(Interaction, spec_set=True)
        view = ActivityView(
            mock_bot,
            mock_interaction,
            MagicMock(latest_username="Foo"),
            datetime.fromtimestamp(100),
            datetime.fromtimestamp(200),
        )
        view._repo.get_playtime_between_period = AsyncMock(
            return_value=timedelta(minutes=61)
        )
        embed_ins = mock_embed.return_value
        # Act
        await view.run()
        # Assert
        mock_embed.assert_called_once_with(
            mock_interaction, title="Player Activity (Foo)", color=Color.teal()
        )
        self.assertEqual(
            embed_ins.description,
            "`Playtime : ` 1h 1m\n" "`Period   : ` <t:100:R> to <t:200:R>",
        )
        embed_ins.finalize.assert_called_once()
        mock_interaction.send.assert_awaited_once_with(embed=mock_embed.return_value)
