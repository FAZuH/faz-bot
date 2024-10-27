import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config

# Necessary to load the models
from fazutil.db.fazdb.fazdb_database import FazdbDatabase
from fazutil.db.fazdb.model.base_fazdb_model import BaseFazdbModel

FazdbDatabase  # prevent being removed by linter lol

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


def get_url():
    """Override sqlalchemy.url with environment variables if set"""
    user = os.getenv("MYSQL_USER", None)
    password = os.getenv("MYSQL_PASSWORD", None)
    host = os.getenv("MYSQL_HOST", None)
    db_name = os.getenv("MYSQL_FAZDB_DATABASE", None)

    if None in {user, password, host, db_name}:
        section = config.get_section(config.config_ini_section)
        assert section is not None
        return section["sqlalchemy.url"]

    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"


# Override the sqlalchemy.url in the alembic.ini
config.set_main_option("sqlalchemy.url", get_url())


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseFazdbModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()  # Use the environment-based URL here too
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    section = config.get_section(config.config_ini_section)
    section["sqlalchemy.url"] = get_url()

    engine = engine_from_config(section, prefix="sqlalchemy.")

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
