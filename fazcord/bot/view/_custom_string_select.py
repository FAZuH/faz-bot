from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, List, Optional

from nextcord.components import SelectOption
from nextcord.ui import StringSelect, View
from nextcord.utils import MISSING


class CustomStringSelect[T: Enum](StringSelect, ABC):

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
        if view is not MISSING:
            view.add_item(self)
        if callback is not MISSING:
            self.callback = callback

        select_options: List[SelectOption] = [
            SelectOption(label=option.value, value=option.name)
            for option in self.option_enum
        ]

        super().__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=select_options,
            disabled=disabled,
            row=row,
        )

    def get_selected_option(self) -> T:
        if len(self.values) == 0:
            raise ValueError("No option selected")
        for option in self.option_enum:
            if option.name == self.values[0]:
                return option
        raise ValueError("Invalid option selected")

    @property
    @abstractmethod
    def option_enum(self) -> type[T]: ...
