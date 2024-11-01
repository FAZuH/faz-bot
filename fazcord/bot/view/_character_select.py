from typing import override


from fazcord.bot.view._character_select_options import CharacterSelectOptions
from fazcord.bot.view._custom_string_select import CustomStringSelect


class CharacterSelect(CustomStringSelect[CharacterSelectOptions]):

    @property
    @override
    def option_enum(self) -> type[CharacterSelectOptions]:
        return CharacterSelectOptions
