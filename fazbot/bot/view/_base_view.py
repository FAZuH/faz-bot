from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, override

from nextcord.ui import View

from fazbot.bot.view._asset import Asset

if TYPE_CHECKING:
    from nextcord import Embed, File, Interaction

    from fazbot.bot.bot import Bot


class BaseView(View, ABC):

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        *,
        timeout: float | None = 180.0,
        auto_defer: bool = True,
        prevent_update: bool = True,
    ) -> None:
        super().__init__(
            timeout=timeout, auto_defer=auto_defer, prevent_update=prevent_update
        )
        self._bot = bot
        self._interaction = interaction

    @abstractmethod
    async def run(self): ...

    @override
    async def on_timeout(self) -> None:
        await self._interaction.edit_original_message(view=View(timeout=1))

    @staticmethod
    def _set_embed_thumbnail_with_asset(embed: Embed, filename: str) -> None:
        embed.set_thumbnail(url=f"attachment://{filename}")

    @staticmethod
    def _get_from_assets(assets: dict[str, File], key: str) -> Asset:
        """Helper method to get an asset.
        Normally only be used inside `_set_assets()`

        Args:
            assets (dict[str, File]): asset dictionary. Normally obtained from `_set_assets()`
            key (str): The file name of the asset.

        Returns:
            Asset: The asset object containing File object and the file name
        """
        file = assets.get(key, None)
        if not file:
            raise KeyError(f"Asset with key {key} doesn't exist.")
        asset = Asset(file, key)
        return asset

    @classmethod
    def set_assets(cls, assets: dict[str, File]) -> None: ...
