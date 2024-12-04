from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any, override, TYPE_CHECKING

from nextcord.ui import Button
from nextcord.ui import View

if TYPE_CHECKING:
    from nextcord import Interaction

    from faz.bot.app.discord.bot.bot import Bot


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
        super().__init__(timeout=timeout, auto_defer=auto_defer, prevent_update=prevent_update)
        self._interaction = interaction
        self._bot = bot

    @abstractmethod
    async def run(self) -> None:
        """Abstract method to run the view.

        This method must be implemented in subclasses to define the behavior of the view.
        """
        ...

    @property
    def bot(self) -> Bot:
        """Bot: The bot instance associated with this interaction.

        Returns:
            Bot: The bot instance currently interacting with this view.
        """
        return self._bot

    @property
    def interaction(self) -> Interaction:
        """Interaction: The interaction instance triggering this view.

        Returns:
            Interaction: The specific interaction tied to the current view state.
        """
        return self._interaction

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
        self.clear_items()
        await self._interaction.edit_original_message(view=self)
