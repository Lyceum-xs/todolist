import pytest
from src.app.db import create_tables, drop_tables

@pytest.fixture(autouse=True)
def setup_db_session():
    """
    此设置在每次测试前运行。
    它使用应用自身的函数来确保数据库被正确清空和重建。
    """
    # 1. 清空所有旧表
    drop_tables()
    # 2. 使用应用自己的函数创建所有新表
    create_tables()
    
    yield
    
    # 3. 测试结束后，再次清空所有表
    drop_tables()