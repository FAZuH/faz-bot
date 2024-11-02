from typing import Any, Callable, Optional, override

from nextcord.ui import View
from nextcord.utils import MISSING

from fazcord.bot.view._categorical_id_select_options import CategoricalIdSelectOptions
from fazcord.bot.view._custom_string_select import CustomStringSelect


class CategoricalIdSelect(CustomStringSelect[CategoricalIdSelectOptions]):

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
        placeholder = placeholder or "Select categorical id"
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
    def option_enum(self) -> type[CategoricalIdSelectOptions]:
        return CategoricalIdSelectOptions
