from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("faz-bot-app-discord")
except PackageNotFoundError:
    __version__ = "development"
