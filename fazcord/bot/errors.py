from nextcord import ApplicationError


class BotException(Exception):
    """Base exception for all exceptions in fazcord.bot package"""

    # def __init__(self, *args):
    #     if message:
    #         message = f"{self.__class__.__doc__}\n{message}"
    #     else:
    #         message = self.__class__.__doc__
    #     super().__init__(message, args)


class ApplicationException(BotException, ApplicationError): ...


class ArgumentValidationFailure(ApplicationException): ...


class ParseFailure(ApplicationException): ...


class BadArgument(ApplicationException): ...
