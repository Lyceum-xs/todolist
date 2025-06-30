"""
Alembic 环境脚本
----------------
负责加载项目中的 SQLAlchemy `engine` 与 `MetaData`，
并在执行 `alembic revision` / `alembic upgrade` 时
提供联机（Online）和离线（Offline）两种迁移模式。
"""
from logging.config import fileConfig
import sys, os

from alembic import context
from sqlalchemy import pool

# 让 src.app 能被导入
sys.path.append(os.getcwd())

# 复用项目里的 engine 和 Base
from src.app.db import engine
from src.app.models import Base

# --- Alembic 配置对象 ---
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 提供给 --autogenerate 的元数据
target_metadata = Base.metadata

# --------------------------------------------------------------------------- #
# 离线模式：生成 SQL 文件
# --------------------------------------------------------------------------- #
def run_migrations_offline() -> None:
    """离线模式：只生成 SQL，不直接连接数据库。"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# --------------------------------------------------------------------------- #
# 在线模式：直接连接数据库并执行迁移
# --------------------------------------------------------------------------- #
def run_migrations_online() -> None:
    """在线模式：使用项目 engine，在事务中执行迁移。"""
    # 如果想通过 alembic.ini 指定其它数据库，可改为 engine_from_config
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,        # 字段类型变化也能检测
        )
        with context.begin_transaction():
            context.run_migrations()

# --------------------------------------------------------------------------- #
# 入口
# --------------------------------------------------------------------------- #
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()