from typing import Any, Callable, override

from faz.bot.app.discord.select.custom_string_select import CustomStringSelect
from faz.bot.app.discord.select.member_history_mode_option import MemberHistoryModeOption


class MemberHistoryModeSelect(CustomStringSelect[MemberHistoryModeOption]):
    def __init__(self, callback: Callable[..., Any]) -> None:
        super().__init__(placeholder="Select mode")
        self.callback = callback

    @property
    @override
    def option_enum(self) -> type[MemberHistoryModeOption]:
        return MemberHistoryModeOption
