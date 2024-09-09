from nextcord import ApplicationCheckFailure, ApplicationError


class ApplicationException(ApplicationError): ...


class InvalidArgumentException(ApplicationException):
    """An invalid command argument."""


class InvalidActionException(ApplicationException):
    """An invalid action or task attempted by the command."""


class ParseException(ApplicationException):
    """A parsing error of a command argument."""


class UnauthorizedUserException(ApplicationCheckFailure):
    """A user with insufficient permissions attempted to execute the command."""


class UnauthorizedLocationException(ApplicationCheckFailure):
    """A command was executed in a disallowed location."""
