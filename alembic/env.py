"""Pylons bootstrap environment.

Place 'pylons_config_file' into alembic.ini, and the application will
be loaded from there.

"""
from alembic import context

from pyramid.paster import get_appsettings
from pyramid.paster import setup_logging

from pyramid_tutorial.models import Base

from sqlalchemy import engine_from_config


config = context.config

app_config_file_name = config.get_main_option("pylons_config_file")

setup_logging(app_config_file_name)

app_settings = get_appsettings(app_config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = app_settings['sqlalchemy.url']
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # specify here how the engine is acquired
    engine = engine_from_config(app_settings, prefix='sqlalchemy.')

    with engine.connect() as connection:  # noqa
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
