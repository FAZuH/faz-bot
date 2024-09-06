from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, override

from nextcord.ui import Button, View

if TYPE_CHECKING:
    from nextcord import Interaction

    from fazcord.bot.bot import Bot


class BaseView(View, ABC):
    """Base class for creating views in a Discord bot using Nextcord.

    This class provides a structure for creating interactive views that can be used
    in Discord messages. It includes a timeout mechanism, automatic deferral, and
    methods to handle button clicks.

    Attributes:
        bot (Bot): The bot instance.
        interaction (Interaction[Any]): The interaction object from Discord.
        timeout (float | None): The timeout period for the view, in seconds. Defaults to 180.0.
        auto_defer (bool): Whether to automatically defer the interaction. Defaults to True.
        prevent_update (bool): Whether to prevent updates to the interaction. Defaults to True.
    """

    def __init__(
        self,
        bot: Bot,
        interaction: Interaction[Any],
        *,
        timeout: float | None = 180.0,
        auto_defer: bool = True,
        prevent_update: bool = True,
    ) -> None:
        """Initializes the BaseView.

        Args:
            bot (Bot): The bot instance.
            interaction (Interaction[Any]): The interaction object from Nextcord.
            timeout (float | None, optional): The timeout period for the view, in seconds.
                Defaults to 180.0.
            auto_defer (bool, optional): Whether to automatically defer the interaction.
                Defaults to True.
            prevent_update (bool, optional): Whether to prevent updates to the interaction.
                Defaults to True.
        """
        super().__init__(
            timeout=timeout, auto_defer=auto_defer, prevent_update=prevent_update
        )
        self._bot = bot
        self._interaction = interaction

    def _click_button(self, button: Button[Any]) -> None:
        """Modifies clicked button appearance by enabling all buttons and
        disabling the clicked button.

        Args:
            button (Button[Any]): The button that was clicked.
        """
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = False
        button.disabled = True

    @override
    async def on_timeout(self) -> None:
        """Handles the timeout event for the view.

        This method is called when the view times out. It updates the original message to
        remove the view.
        """
        await self._interaction.edit_original_message(view=View(timeout=1))

    @abstractmethod
    async def run(self):
        """Abstract method to run the view.

        This method must be implemented in subclasses to define the behavior of the view.
        """
        ...
