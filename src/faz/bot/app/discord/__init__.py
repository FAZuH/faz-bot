from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    __version__ = version("faz-bot-app-discord")
except PackageNotFoundError:
    __version__ = "development"
