# To-Do List 项目

这是一个基于 Python 的待办事项管理程序，支持命令行和未来扩展的图形界面，涵盖任务管理、标签、搜索、习惯打卡、日历视图等功能。
> 这是初版的项目结构和README文档，后续可能根据实际情况有所调整  
> 项目的整体结构参考了比较成熟的项目架构，较为复杂，后续会根据实际情况进行调整
## 项目目标
#### 待办事项处理
- 添加新的待办事项（支持任务描述、可选截止日期）。
- 列出所有待办事项（支持按状态、截止日期排序）。
- 标记某个事项为“已完成”或“未完成”。
- 删除某个事项。
- 主任务可细分为子任务（当前支持一层树形结构）。
- 根据名称搜索任务。
- 任务排序（可选优先参数、排序）

#### 页面设计
- 支持导航栏。
- 横屏、竖屏模式适配。

#### 额外功能
- 每日习惯打卡
- 跟日历结合做一个日历视图
- 番茄钟功能

#### 其他要求
- 数据持久化存储。
- 通过Python打包工具进行打包。

## 项目技术栈
#### 版本 1.0 (当前)

| 组件       | 技术选择       | 说明                          |
|------------|----------------|-------------------------------|
| **前端**   | Tkinter        | Python内置GUI框架             |
| **后端**   | Python         | 核心业务逻辑实现              |
| **数据库** | SQLite         | 轻量级嵌入式数据库            |
| **打包**   | PyInstaller    | 生成可执行文件                |
| **测试**   | pytest         | 单元测试框架                  |

#### 版本 2.0 (规划中)

| 组件       | 技术选择               | 说明                          |
|------------|------------------------|-------------------------------|
| **前端**   | HTML + JavaScript      | 现代化Web界面                 |
| **后端**   | FastAPI                | 高性能Python API框架          |
| **数据库** | SQLite                 |  轻量级嵌入式数据库          |
| **架构**   | 前后端分离             |                |
| **打包**   | Docker                 | 容器化部署方案                |
| **测试**   | pytest                | 全栈测试方案                  |

## 项目结构

```
todolist/
├─ docs/                     # 项目文档目录
│  ├─ design.md              # 设计文档
│  └─ user_guide.md          # 用户手册
├─ Jenkinsfile               # CI/CD 配置文件
├─ pyproject.toml            # Python 项目配置文件
├─ README.md                 # 项目说明文件
├─ requirements-dev.txt      # 开发环境依赖
├─ requirements.txt          # 生产环境依赖
├─ src/                      # 源代码主目录
│  ├─ api/                   # API接口相关
│  │  ├─ exceptions.py       # 异常处理
│  │  ├─ stats_api.py        # 统计API
│  │  ├─ task_api.py         # 任务API
│  │  ├─ test_api.py         # API测试
│  │  └─ __init__.py         # 初始化文件
│  ├─ app/                   # 应用核心逻辑
│  │  ├─ crud.py             # 数据库操作
│  │  ├─ db.py               # 数据库连接
│  │  ├─ main.py             # 主程序入口
│  │  ├─ models.py           # 数据模型
│  │  ├─ routers/            # 路由模块
│  │  │  ├─ habits.py        # 习惯路由
│  │  │  ├─ tasks.py         # 任务路由
│  │  │  └─ __init__.py
│  │  ├─ schemas.py          # 数据模式
│  │  ├─ services.py         # 前端接口
│  │  └─ __init__.py
│  ├─ gui/                   # ui界面相关
│  │  ├─ change_data.py      # 数据变更界面
│  │  ├─ content_view.py     # 内容视图
│  │  ├─ get_data.py
│  │  ├─ main_window.py      # 主窗口
│  │  ├─ task_item.py        # 任务项组件
│  │  └─ __init__.py
│  ├─ README.md              # 子目录说明
│  ├─ services/
│  │  ├─ analytics.py
│  │  ├─ notification.py
│  │  └─ __init__.py
│  └─ utils/                 # 工具类
│     ├─ exporters.py
│     ├─ validators.py
│     └─ __init__.py
├─ tasks.json                # 任务数据文件（示例）
└─ tests/                    # 测试目录
   ├─ integration/           # 集成测试
   │  └─ test_gui_integration.py  # GUI集成测试
   └─ unit/                  # 单元测试
      ├─ test_database.py    # 数据库测试
      ├─ test_models.py      # 模型测试
      └─ test_services.py    # 服务测试

```




