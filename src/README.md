Todo Backend (FastAPI + SQLAlchemy)

    •    分层目录结构（app/, app/routers/, app/models.py …）
    •    Pydantic v2 数据验证
    •    默认 SQLite 存储，可随时切换 Postgres / MySQL
⸻

快速启动

#进入代码目录
cd /path/to/todo

#创建并激活虚拟环境（任选 venv/conda/poetry）
python -m venv .venv && source .venv/bin/activate

#安装依赖
pip install -r requirements.txt

#启动开发服务器
uvicorn app.main:app --reload

#打开浏览器
http://127.0.0.1:8000/docs

第一次运行 会在当前目录生成 todo.db（SQLite），表结构自动创建。

⸻

目录结构

├── app/                    # 顶层包
│   ├── __init__.py
│   ├── db.py               # 数据库连接 / Session
│   ├── models.py           # SQLAlchemy ORM 模型
│   ├── schemas.py          # Pydantic v2 数据模型
│   ├── crud.py             # 业务逻辑封装
│   ├── main.py             # FastAPI 应用入口
│   └── routers/
│       ├── __init__.py
│       └── tasks.py        # /tasks* 接口
├── todo.db                 # SQLite 数据库（自动生成）
├── requirements.txt        # 依赖清单
└── README.md               # 项目说明


⸻

主要依赖

库    版本要求    作用
fastapi    ≥0.115    Web 框架，自动生成 OpenAPI
sqlalchemy    ≥2.0    ORM / 数据映射
pydantic    ≥2.6    数据校验与序列化
uvicorn    ≥0.29    ASGI 服务器

具体版本以 requirements.txt 为准，可随时 pip install -U 升级。

⸻

运行模式

开发模式

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

    •    --reload：保存代码自动重启
    •    --host 0.0.0.0：局域网可访问（访问 http://<本机IP>:8000/docs）

生产模式示例

uvicorn app.main:app --host 0.0.0.0 --port 80 --workers 4

建议前置 Nginx / Caddy 处理 TLS 与反向代理。

⸻

API 一览

方法    路径    描述
POST    /tasks    创建任务
GET    /tasks    任务列表（过滤 / 排序）
GET    /tasks/{id}    获取单任务
PATCH    /tasks/{id}    更新任务
DELETE    /tasks/{id}    删除任务
GET    /tasks/search?q=    名称模糊搜索

详细请求 / 响应示例请打开 Swagger-UI。

⸻

数据库迁移

当前示例使用 Base.metadata.create_all() 自动建表。若需正式版本管理，推荐 Alembic：

pip install alembic
alembic init migrations
# 编辑 migrations/env.py 里的 target_metadata
alembic revision --autogenerate -m "init"
alembic upgrade head


⸻

测试

pip install pytest httpx
pytest -q

测试用例示范见 tests/（如需自建）。

⸻

部署参考
    1.    Docker

FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


    2.    Gunicorn + UvicornWorker

gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:80


    3.    云服务：阿里云 ECS / 腾讯云 / Render / Railway 等均可运行。

⸻

常见问题

问题    解决方案
ImportError: attempted relative import beyond top-level package    确保目录层级 / __init__.py 正确，且从项目根启动 uvicorn app.main:app
Swagger-UI 仍显示英文    升级 swagger-ui-bundle>=0.0.18 并在 main.py 设置 swagger_ui_parameters={"locale": "zh-CN"}
SQLite 锁或权限错误    关闭所有连接后删除 todo.db（仅测试环境）重新启动
