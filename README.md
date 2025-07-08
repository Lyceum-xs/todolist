# ToDoList 应用 📝

> 一款集 **桌面 GUI + Web API** 于一体的跨平台任务 / 习惯管理工具
> 采用 **FastAPI + SQLite + Tkinter** 技术栈，开箱即用，适合作为学习全栈开发或个人效率提升的参考项目。

---

## 功能亮点

* **任务管理**：支持新建 / 查询 / 更新 / 删除（CRUD），优先级、截止日期与完成状态跟踪
* **习惯养成**：打卡记录、统计视图，一目了然
* **番茄计时器**：专注 25 min，休息 5 min，助你进入心流
* **多终端交互**

  * 🖥 **Tkinter 桌面端** —— 离线可用的原生体验
  * 🌐 **RESTful API** —— `/docs` 自动生成 Swagger，便于二次开发
  * 💻 **HTML/JS 单页** —— 轻量级 Web 前端（可选）
* **数据持久化**：`SQLite + SQLAlchemy`
* **数据库版本控制**：Alembic
* **代码质量**：pytest + coverage + SonarQube
* **CI/CD**：GitLab CI + Ansible 部署示例
* **MIT License**：自由修改与商用

---

## 技术栈

| 层次     | 技术                                         | 说明              |
| ------ | ------------------------------------------ | --------------- |
| 后端 API | **FastAPI 0.115.x**                        | 高性能异步 Web 框架    |
| ORM    | **SQLAlchemy 2.0**                         | Python 数据库映射    |
| DB     | **SQLite**                                 | 零配置嵌入式数据库       |
| 前端     | **Tkinter / HTML+JS**                      | 桌面 GUI / Web UI |
| 其他     | Alembic、pytest、SonarQube、GitLab CI、Ansible | 运维与保障           |

---

## 环境要求

* **Python ≥ 3.10**（建议 3.12）
* pip / venv 或 Poetry
* *可选*：Git、SonarQube Server、Ansible

---

## 快速开始

```bash
# 1. 克隆仓库
git clone https://whucsgitlab.whu.edu.cn/devops/todolist.git
cd todolist

# 2. 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate

# 3. 安装依赖
pip install -r requirements.txt         # 生产依赖
# pip install -r requirements-dev.txt   # 若需开发 / 测试

# 4. 初始化数据库（自动生成 todo.db）
python init_db.py

# 5. 启动后端（Swagger -> http://127.0.0.1:8000/docs）
uvicorn src.app.main:app --reload

# 6. 启动桌面 GUI（同时守护后端）
python run.py

# 7. 仅运行 Web UI（可选）
python run_html.py
```

> **TIP:** `run.py` 会在后台线程自动拉起 FastAPI 服务，确保桌面端即装即用。

---

## API 预览

| 方法     | 路径            | 描述           |
| ------ | ------------- | ------------ |
| GET    | `/health`     | 健康检查         |
| POST   | `/tasks`      | 创建任务         |
| GET    | `/tasks`      | 任务列表（支持状态过滤） |
| PATCH  | `/tasks/{id}` | 更新任务         |
| DELETE | `/tasks/{id}` | 删除任务         |
| ...    | `/habits`     | 习惯相关接口       |

完整交互请打开浏览器访问 **`/docs`**（Swagger UI）或 **`/redoc`**。

---

## 数据库迁移

```bash
# 生成迁移脚本
alembic revision --autogenerate -m "add priority to tasks"
# 应用到最新
alembic upgrade head
```

---

## 测试 & 代码质量

```bash
# 运行单元测试
pytest -q

# 生成覆盖率报告
pytest --cov=src --cov-report=xml

# 提交 SonarQube（需先配置 sonar-project.properties 与 TOKEN）
sonar-scanner
```

---

## 持续集成 / 部署

* `.gitlab-ci.yml`   ：示例 3 阶段 Pipeline（测试→构建→部署）
* `deploy_todolist.yml`：Ansible Playbook，本地或远程一键部署
* 支持 Docker / systemd 等自定义方案，视需要扩展

---

## 项目结构

```
todolist
├── run.py               # 同时启动后端 + GUI
├── run_html.py          # 启动纯 Web 模式
├── requirements.txt
├── pyproject.toml
├── src/
│   ├── app/             # FastAPI 后端
│   │   ├── routers/
│   │   ├── services.py
│   │   ├── models.py
│   │   ├── db.py
│   │   └── main.py
│   └── gui/             # Tkinter 前端
│       ├── views/
│       ├── widgets/
│       └── main_window.py
├── migrations/          # Alembic 迁移脚本
├── tests/               # pytest 测试
└── docs/                # 额外文档（如 API 说明书）
```

---

## 贡献指南

1. **Fork** → **Create Feature Branch** → **Commit** → **Push** → **Merge Request**
2. 确保 `pytest` 与 `flake8` 通过；如改动数据库需附带 Alembic 迁移
3. 代码会通过 SonarQube 自动扫描，尽量保持 **A 级质量与 0 new bugs** ✨

---

## License

[MIT](LICENSE) © 2025 Lyceum-xs

---

感谢使用 ToDoList，祝你高效每一天！🚀
