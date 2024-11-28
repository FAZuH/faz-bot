from typing import Any, Callable, override

from faz.bot.app.discord.select.custom_string_select import CustomStringSelect
from faz.bot.app.discord.select.guild_history_id_options import GuildHistoryIdOptions


class GuildHistoryIdSelect(CustomStringSelect[GuildHistoryIdOptions]):
    def __init__(self, callback: Callable[..., Any]) -> None:
        super().__init__(placeholder="Select mode")
        self.callback = callback

    @property
    @override
    def option_enum(self) -> type[GuildHistoryIdOptions]:
        return GuildHistoryIdOptions
