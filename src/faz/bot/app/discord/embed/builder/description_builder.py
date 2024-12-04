from copy import copy
from typing import Self


class DescriptionBuilder:
    """A builder class for creating formatted description strings with key-value pairs.

    This class helps in building description strings where each line consists of a key-value pair,
    formatted with consistent spacing and markdown styling.
    """

    def __init__(self, initial_lines: list[tuple[str, str]] | None = None) -> None:
        """Initialize a new DescriptionBuilder instance.

        Args:
            initial_lines (list[tuple[str, str]] | None): Initial list of key-value pairs to populate the builder.
                Defaults to None.
        """
        self._initial_lines = initial_lines or []
        self.reset()  # Copy _initial_lines to _lines

    def add_line(self, key: str, value: str) -> Self:
        """Add a new key-value pair line to the end of the description.

        Args:
            key (str): The key for the line.
            value (str): The value associated with the key.

        Returns:
            Self: The builder instance for method chaining.
        """
        self._lines.append((key, value))
        return self

    def insert_line(self, index: int, key: str, value: str) -> Self:
        """Insert a new key-value pair line at the specified index.

        Args:
            index (int): The position where the new line should be inserted.
            key (str): The key for the line.
            value (str): The value associated with the key.

        Returns:
            Self: The builder instance for method chaining.
        """
        self._lines.insert(index, (key, value))
        return self

    def remove_line(self, index: int) -> Self:
        """Remove a line at the specified index.

        Args:
            index (int): The index of the line to remove.

        Returns:
            Self: The builder instance for method chaining.
        """
        self._lines.pop(index)
        return self

    def remove_line_by_key(self, key: str) -> Self:
        """Remove all lines that match the specified key.

        Args:
            key (str): The key to match for removal.

        Returns:
            Self: The builder instance for method chaining.
        """
        self._lines = [line for line in self._lines if line[0] != key]
        return self

    def reset(self) -> Self:
        """Reset the builder to its initial state.

        Returns:
            Self: The builder instance for method chaining.
        """
        self._lines = copy(self._initial_lines)
        return self

    def build(self) -> str:
        """Build and return the formatted description string.

        The resulting string will have each key-value pair on a new line,
        with keys right-padded to ensure alignment.

        Returns:
            str: The formatted description string.
        """
        key_size = self._get_longest_key()
        ret = "\n".join(f"`{k.ljust(key_size)} :` {v}" for k, v in self._lines)
        return ret

    def set_builder_initial_lines(self, initial_lines: list[tuple[str, str]]) -> Self:
        """Set new initial lines for the builder.

        Args:
            initial_lines (list[tuple[str, str]]): New list of key-value pairs to set as initial lines.

        Returns:
            Self: The builder instance for method chaining.
        """
        self._initial_lines = initial_lines
        return self

    def _get_longest_key(self) -> int:
        """Get the length of the longest key in the current lines.

        Returns:
            int: Length of the longest key.
        """
        return len(max(self._lines, key=lambda x: len(x[0]))[0])
