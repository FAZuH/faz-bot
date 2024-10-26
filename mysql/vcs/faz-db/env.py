import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# from fazutil.db.fazdb.model.base_fazdb_model import BaseFazdbModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Override sqlalchemy.url with environment variables
def get_url():
    user = os.getenv("MYSQL_USER", "faz")
    password = os.getenv("MYSQL_PASSWORD", "password")
    host = os.getenv("MYSQL_HOST", "localhost")
    db_name = os.getenv("MYSQL_FAZDB_DATABASE", "faz-db")  # Default fallback
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"


# Override the sqlalchemy.url in the alembic.ini
config.set_main_option("sqlalchemy.url", get_url())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
# target_metadata = BaseFazdbModel.metadata
target_metadata = None


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
    # Use the environment-based URL for the configuration
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
