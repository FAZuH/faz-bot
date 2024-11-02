from typing import Any, Callable, Optional, override

from nextcord.ui import View
from nextcord.utils import MISSING

from fazcord.bot.view._custom_string_select import CustomStringSelect
from fazcord.bot.view._numerical_id_select_options import IdSelectOptions


class IdSelect(CustomStringSelect[IdSelectOptions]):

    def __init__(
        self,
        *,
        view: View = MISSING,
        callback: Callable[..., Any] = MISSING,
        custom_id: str = MISSING,
        placeholder: Optional[str] = None,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        placeholder = placeholder or "Select ID"
        super().__init__(
            view=view,
            callback=callback,
            custom_id=custom_id,
            placeholder=placeholder,
            disabled=disabled,
            row=row,
        )

    @property
    @override
    def option_enum(self) -> type[IdSelectOptions]:
        return IdSelectOptions
