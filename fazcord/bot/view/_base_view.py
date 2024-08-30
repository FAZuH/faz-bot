from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, override

from nextcord.ui import Button, View

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazcord.bot.bot import Bot


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

    def _click_button(self, button: Button[Any]) -> None:
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = False
        button.disabled = True

    @override
    async def on_timeout(self) -> None:
        await self._interaction.edit_original_message(view=View(timeout=1))

    @abstractmethod
    async def run(self): ...
