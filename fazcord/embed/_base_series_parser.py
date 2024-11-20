from abc import ABC
from typing import Any, MutableSequence

from fazcord.embed.embed_field import EmbedField


class BaseSeriesParser(ABC):

    def _common_numerical_float_string_parser(
        self, timestamp: str, value: float
    ) -> str:
        ret = f"{timestamp}: `{value:.2f}`"
        return ret

    def _common_numerical_int_string_parser(self, timestamp: str, value: int) -> str:
        ret = f"{timestamp}: `{value}`"
        return ret

    @staticmethod
    def _add_embed_field(
        container: MutableSequence[EmbedField], label: str, value: str
    ) -> None:
        """Handles max embed value limit of 1024 characters."""
        while True:
            idx = value.rfind("\n", 0, 1024)
            if idx == -1:
                break
            container.append(EmbedField(name=label, value=value[:idx]))
            label = ""  # Only the first field has a label
            value = value[idx + 1 :]
            if len(value) <= 1024:
                break

    @staticmethod
    def _get_max_key_length(dict_: dict[str, Any]) -> int:
        return max(map(len, dict_.keys()))

    @staticmethod
    def _diff_str_or_blank(value: str, label: str, label_space: int) -> str:
        return f"`{label:{label_space}} : ` {value}"

    @staticmethod
    def _format_number(value: Any) -> str:
        return f"{value:,}" if isinstance(value, int) else f"{value:,.2f}"
