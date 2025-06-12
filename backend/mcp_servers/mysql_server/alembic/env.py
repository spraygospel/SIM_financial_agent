# File: backend/mcp_servers/mysql_server/alembic/env.py (v1.2 - Final)

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- Alembic Config ---
import os
import sys

# Menambahkan root proyek ke sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

# Impor Base dari model ORM kita dan pastikan semua model ter-load
from backend.mcp_servers.mysql_server.db_models import Base
target_metadata = Base.metadata

# Impor settings untuk mendapatkan URL database
from backend.app.core.config import settings
# --- AKHIR Alembic Config ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata di-set di atas dari model kita
# target_metadata = None


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
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
    
    # Set opsi utama untuk koneksi database dari settings kita
    config.set_main_option('DB_CONNECTION_STRING', settings.DATABASE_URL)
    
    # --- REVISI DI SINI ---
    # Dapatkan section config yang benar ('alembic') tanpa duplikasi argumen
    alembic_config_section = config.get_section(config.config_ini_section)
    
    # Atur url sqlalchemy di dalam section config tersebut
    alembic_config_section['sqlalchemy.url'] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        alembic_config_section, # Gunakan section yang sudah kita siapkan
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()