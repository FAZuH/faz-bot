from typing import Any, Callable, Optional, override

from nextcord import SelectOption
from nextcord.utils import MISSING

from faz.bot.app.discord.select.custom_string_select import CustomStringSelect
from faz.bot.app.discord.select.player_history_data_options import PlayerHistoryDataOptions


class PlayerHistoryDataSelect(CustomStringSelect[PlayerHistoryDataOptions]):
    def __init__(
        self,
        callback: Callable[..., Any],
        *,
        custom_id: str = MISSING,
        placeholder: Optional[str] = None,
        min_values: int = 1,
        max_values: int = 1,
        options: list[SelectOption] = MISSING,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        placeholder = placeholder or "Select ID"
        super().__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
            disabled=disabled,
            row=row,
        )
        self.callback = callback

    @override
    def _get_select_options(self) -> list[SelectOption]:
        ret = [
            SelectOption(label=option.value.value, value=option.name) for option in self.option_enum
        ]
        return ret

    @property
    @override
    def option_enum(self) -> type[PlayerHistoryDataOptions]:
        return PlayerHistoryDataOptions
