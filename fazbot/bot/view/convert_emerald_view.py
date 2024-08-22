from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from nextcord import Embed, Interaction

from fazbot.bot.view._base_view import BaseView
from fazbot.wynn.emerald_util import EmeraldUtil
from fazbot.wynn.emeralds import Emeralds

if TYPE_CHECKING:
    from nextcord import File

    from fazbot.bot.bot import Bot
    from fazbot.bot.view._asset import Asset


class ConvertEmeraldView(BaseView):

    ASSET_LIQUIDEMERALD: Asset

    def __init__(
        self, bot: Bot, interaction: Interaction[Any], emerald_string: str
    ) -> None:
        super().__init__(bot, interaction)
        self._emerald_string = emerald_string
        self._emeralds = Emeralds.from_string(emerald_string)
        self._emeralds.simplify()

    @override
    @classmethod
    def set_assets(cls, assets: dict[str, File]) -> None:
        cls.ASSET_LIQUIDEMERALD = cls._get_from_assets(assets, "liquidemerald.png")

    @override
    async def run(self):
        embed_resp = self._get_embed(self._interaction, self._emeralds)
        await self._interaction.send(
            embed=embed_resp, file=self.ASSET_LIQUIDEMERALD.get_file_to_send()
        )

    def _get_embed(self, interaction: Interaction[Any], emeralds: Emeralds) -> Embed:
        set_price_tm, set_price_silverbull = EmeraldUtil.get_set_price(emeralds)
        embed_resp = Embed(title="Emerald Convertor", color=8894804)

        self._set_embed_thumbnail_with_asset(
            embed_resp, self.ASSET_LIQUIDEMERALD.filename
        )
        embed_resp.description = (
            f"Converted: **{emeralds}**\n" f"Emeralds Total: **{emeralds.total}e**"
        )
        embed_resp.add_field(
            name="TM Set Price", value=f"{set_price_tm.emeralds}", inline=True
        )
        embed_resp.add_field(
            name="Silverbull Set Price",
            value=f"{set_price_silverbull.emeralds}",
            inline=True,
        )
        if interaction.user:
            embed_resp.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.display_avatar.url,
            )
        return embed_resp
