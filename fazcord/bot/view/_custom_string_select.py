from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, List, Optional

from nextcord.components import SelectOption
from nextcord.ui import StringSelect
from nextcord.utils import MISSING


class CustomStringSelect[T: Enum](StringSelect, ABC):

    def __init__(
        self,
        callback: Callable[..., Any] | None = None,
        *,
        custom_id: str = MISSING,
        placeholder: Optional[str] = None,
        min_values: int = 1,
        max_values: int = 1,
        options: List[SelectOption] = MISSING,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        select_options = self._get_select_options()
        super().__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options or select_options,
            disabled=disabled,
            row=row,
        )
        if callback:
            self.callback = callback

    def get_selected_option(self) -> T:
        if len(self.values) == 0:
            raise ValueError("No option selected")
        for option in self.option_enum:
            if option.name == self.values[0]:
                return option
        raise ValueError("Invalid option selected")

    def _get_select_options(self) -> list[SelectOption]:
        ret = [
            SelectOption(label=option.value, value=option.name)
            for option in self.option_enum
        ]
        return ret

    @property
    @abstractmethod
    def option_enum(self) -> type[T]: ...
