class EmbedField:
    __slots__ = ("_name", "_value", "_inline")

    def __init__(self, name: str, value: str, inline: bool = False) -> None:
        self._name = name
        self._value = value
        self._inline = inline

    @property
    def name(self):
        """The name property."""
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def value(self):
        """The value property."""
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    @property
    def inline(self):
        """The inline property."""
        return self._inline

    @inline.setter
    def inline(self, value) -> None:
        self._inline = value
