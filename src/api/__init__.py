"""
API 子包初始化

此模块用于聚合对外暴露的 FastAPI 路由。

用法示例：
    from src.api import router
    app.include_router(router)
"""

# 如果已有版本化子路由，可在此统一暴露
# 例：
# from .v1 import router as v1_router
# router = v1_router
#
# __all__ = ["router"]
