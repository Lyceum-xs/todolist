from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import habits 
from .db import create_tables
from .routers import tasks

tags_metadata = [
    {"name": "任务", "description": "任务相关接口（创建 / 查询 / 更新 / 删除 / 搜索）"}
]

app = FastAPI(
    title="待办事项后端",
    description="一个简洁的 Todo-List API，用于演示 FastAPI + SQLAlchemy 的中文化接口。",
    version="0.1.0",
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "locale": "zh-CN",
        "docExpansion": "none",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 指定前端域名
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(habits.router)

@app.on_event("startup")
def init_db():
    create_tables()