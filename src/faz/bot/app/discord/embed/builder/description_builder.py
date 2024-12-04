from copy import copy
from typing import Self


class DescriptionBuilder:
    def __init__(self, initial_lines: list[tuple[str, str]] | None = None) -> None:
        self._initial_lines = initial_lines or []
        self._lines: list[tuple[str, str]] = []

    def add_line(self, key: str, value: str) -> Self:
        self._lines.append((key, value))
        return self

    def insert_line(self, index: int, key: str, value: str) -> Self:
        self._lines.insert(index, (key, value))
        return self

    def remove_line(self, index: int) -> Self:
        self._lines.pop(index)
        return self

    def remove_line_by_key(self, key: str) -> Self:
        self._lines = [line for line in self._lines if line[0] != key]
        return self

    def reset(self) -> Self:
        self._lines = copy(self._initial_lines)
        return self

    def build(self) -> str:
        key_size = self._get_longest_key()
        ret = "\n".join(f"`{k.ljust(key_size)} :` {v}" for k, v in self._lines)
        return ret

    def set_builder_initial_lines(self, initial_lines: list[tuple[str, str]]) -> Self:
        self._initial_lines = initial_lines
        return self

    def _get_longest_key(self) -> int:
        return len(max(self._lines, key=lambda x: len(x[0]))[0])
