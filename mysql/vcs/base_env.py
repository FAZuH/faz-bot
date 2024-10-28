import os
from abc import ABC, abstractmethod
from logging.config import fileConfig

from alembic import context
from alembic.config import Config
from sqlalchemy import MetaData, engine_from_config


class BaseEnv(ABC):
    def __init__(self) -> None:
        self._config = context.config

    def run(self) -> None:
        # Override the sqlalchemy.url in the alembic.ini
        self.config.set_main_option("sqlalchemy.url", self._get_url())

        # Interpret the config file for Python logging.
        # This line sets up loggers basically.
        if self.config.config_file_name is not None:
            fileConfig(self.config.config_file_name)

        if context.is_offline_mode():
            self._run_migrations_offline()
        else:
            self._run_migrations_online()

    def _get_url(self):
        """Override sqlalchemy.url with environment variables if set"""
        user = os.getenv("MYSQL_USER", None)
        password = os.getenv("MYSQL_PASSWORD", None)
        host = os.getenv("MYSQL_HOST", None)
        db_name = os.getenv("MYSQL_FAZCORD_DATABASE", None)

        if None in {user, password, host, db_name}:
            section = self.config.get_section(self.config.config_ini_section)
            assert section is not None
            return section["sqlalchemy.url"]

        return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

    def _run_migrations_offline(self) -> None:
        """Run migrations in 'offline' mode."""
        url = self._get_url()  # Use the environment-based URL here too
        context.configure(
            url=url,
            target_metadata=self.metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

    def _run_migrations_online(self) -> None:
        """Run migrations in 'online' mode."""
        section = self.config.get_section(self.config.config_ini_section)
        assert section
        section["sqlalchemy.url"] = self._get_url()

        engine = engine_from_config(section, prefix="sqlalchemy.")

        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=self.metadata)

            with context.begin_transaction():
                context.run_migrations()

    @property
    @abstractmethod
    def metadata(self) -> MetaData:
        pass

    @property
    def config(self) -> Config:
        return self._config
