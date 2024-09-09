from collections.abc import Sequence
from datetime import datetime, timezone
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, create_autospec, patch

from nextcord import Interaction

from fazcord.bot.view.stat_worldlist_view import StatWorldlistView


class TestStatWorldlistView(IsolatedAsyncioTestCase):
    @patch("fazcord.bot.view.stat_worldlist_view.PaginationEmbed")
    async def test_run(self, mock_embed: MagicMock) -> None:
        # Prepare
        mock_bot = MagicMock()
        mock_interaction = create_autospec(Interaction, spec_set=True)
        mock_interaction.created_at = datetime.fromtimestamp(600).replace(
            tzinfo=timezone.utc
        )
        mock_bot.fazdb_db.worlds_repository.get_worlds = AsyncMock(
            return_value=self._get_mock_worlds()
        )
        view = StatWorldlistView(mock_bot, mock_interaction, "Player Count")
        embed_ins = MagicMock()
        embed_ins.get_items.return_value = self._get_mock_worlds()
        mock_embed.return_value.get_base.return_value = embed_ins
        # Act
        await view.run()
        # Assert
        self.assertMultiLineEqual(
            embed_ins.description,
            "```ml\n"
            "|   No | World   |   Players | Uptime   |\n"
            "|------|---------|-----------|----------|\n"
            "|    1 | WC10    |        10 | 10m      |\n"
            "|    2 | WC11    |        20 | 9m       |\n"
            "|    3 | WC12    |        30 | 8m       |\n"
            "|    4 | WC13    |        40 | 7m       |\n"
            "|    5 | WC14    |        50 | 6m       |\n"
            "```",
        )
        self.assertEqual(embed_ins.current_page, 1)
        embed_ins.finalize.assert_called_once()
        mock_interaction.send.assert_awaited_once_with(embed=embed_ins, view=view)

    def _get_mock_worlds(self) -> Sequence[MagicMock]:
        ret = []
        ts = lambda t: datetime.fromtimestamp(t)
        ret.append(self._create_mock_world("WC10", 10, ts(0)))
        ret.append(self._create_mock_world("WC11", 20, ts(60)))
        ret.append(self._create_mock_world("WC12", 30, ts(120)))
        ret.append(self._create_mock_world("WC13", 40, ts(180)))
        ret.append(self._create_mock_world("WC14", 50, ts(240)))
        return ret

    @staticmethod
    def _create_mock_world(
        name: str, player_count: int, time_created: datetime
    ) -> MagicMock:
        mock = MagicMock()
        mock.name = name
        mock.player_count = player_count
        mock.time_created = time_created
        return mock
