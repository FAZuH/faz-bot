from typing import override


from fazcord.bot.view._custom_string_select import CustomStringSelect
from fazcord.bot.view._data_type_select_options import DataTypeSelectOptions


class DataTypeSelect(CustomStringSelect[DataTypeSelectOptions]):

    @property
    @override
    def option_enum(self) -> type[DataTypeSelectOptions]:
        return DataTypeSelectOptions
