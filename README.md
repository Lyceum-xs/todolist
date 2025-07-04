# To-Do List 项目

这是一个基于 Python 的待办事项管理程序，支持命令行和未来扩展的图形界面，涵盖任务管理、标签、搜索、习惯打卡、日历视图等功能。
> 这是初版的项目结构和README文档，后续可能根据实际情况有所调整  
> 项目的整体结构参考了比较成熟的项目架构，较为复杂，后续会根据实际情况进行调整

## 项目文件
储存在doc目录下

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
#### 版本 1.0

| 组件       | 技术选择       | 说明                          |
|------------|----------------|-------------------------------|
| **前端**   | Tkinter        | Python内置GUI框架             |
| **后端**   | Python         | 核心业务逻辑实现              |
| **数据库** | SQLite         | 轻量级嵌入式数据库            |
| **打包**   | PyInstaller    | 生成可执行文件                |
| **测试**   | pytest         | 单元测试框架                  |

#### 版本 2.0

| 组件       | 技术选择               | 说明                          |
|------------|------------------------|-------------------------------|
| **前端**   | HTML + JavaScript      | 现代化Web界面                 |
| **后端**   | FastAPI                | 高性能Python API框架          |
| **数据库** | SQLite                 |  轻量级嵌入式数据库          |
| **架构**   | 前后端分离             |                |
| **打包**   | PyInstaller           | 生成可执行文件                |
| **测试**   | pytest                | 全栈测试方案                  |

## 项目结构

```
todolist/
├── .github/                       # GitHub工作流配置
│   └── workflows/
│       └── ci.yml                 # 持续集成流程
├── alembic.ini                    # Alembic数据库迁移工具配置
├── api测试报告.md                 # API测试报告
├── deploy_todolist.yml            # 项目部署配置
├── docs/                          # 项目文档
│   ├── design.md                  # 系统设计文档
│   └── user_guide.md              # 用户使用指南
├── html/                          # 前端静态资源
│   ├── index.html                 # 前端主页
│   ├── script.js                  # 前端JavaScript脚本
│   └── style.css                  # 前端样式表
├── migrations/                    # 数据库迁移脚本
│   ├── env.py                     # Alembic环境配置
│   ├── README                     # 迁移目录说明
│   └── script.py.mako             # Alembic脚本模板
├── pyproject.toml                 # Python项目配置
├── pytest.ini                     # Pytest测试框架配置
├── README.md                      # 项目总览及快速入门
├── requirements-dev.txt           # 开发环境依赖
├── requirements.txt               # 生产环境依赖
├── resources/                     # 静态资源文件
│   ├── icons/                     # 图标文件
│   └── styles/                    # 样式文件
│       └── theme.css              # 主题样式表
├── run.py                         # 项目启动脚本
├── scripts/                       # 自动化脚本
│   ├── build.sh                   # 构建脚本
│   ├── deploy.sh                  # 部署脚本
│   └── test_runner.py             # 测试运行器
├── setup.py                       # Python包安装配置
├── sonar-project.properties       # SonarQube代码分析配置
├── src/                           # 源代码主目录
│   ├── app/                       # 后端应用模块
│   │   ├── crud.py                # 数据库增删改查操作
│   │   ├── db.py                  # 数据库连接与会话
│   │   ├── main.py                # 后端应用入口
│   │   ├── models.py              # 数据库模型定义
│   │   ├── routers/               # API路由定义
│   │   │   ├── habits.py          # 习惯相关路由
│   │   │   ├── tasks.py           # 任务相关路由
│   │   │   └── __init__.py        # Python包标识
│   │   ├── schemas.py             # 数据校验模型
│   │   ├── services.py            # 业务逻辑服务
│   │   └── __init__.py            # Python包标识
│   ├── gui/                       # 图形用户界面(GUI)模块
│   │   ├── main_window.py         # GUI主窗口
│   │   ├── services.py            # GUI业务逻辑
│   │   ├── utils.py               # GUI工具函数
│   │   ├── views/                 # GUI视图模块
│   │   │   ├── calendar.py        # 日历视图
│   │   │   ├── habitclockin.py    # 习惯打卡视图
│   │   │   ├── home.py            # 主页视图
│   │   │   ├── timer.py           # 计时器视图
│   │   │   └── __init__.py        # Python包标识
│   │   ├── widgets/               # GUI自定义组件
│   │   │   ├── content_bar.py     # 内容栏组件
│   │   │   ├── navigation_bar.py  # 导航栏组件
│   │   │   ├── title_bar.py       # 标题栏组件
│   │   │   └── __init__.py        # Python包标识
│   │   └── __init__.py            # Python包标识
│   ├── README.md                  # src目录说明
│   └── __init__.py                # Python包标识
├── tasks.json                     # VS Code任务配置
└── tests/                         # 测试文件
    ├── conftest.py                # Pytest共享配置
    ├── integration/               # 集成测试
    │   └── test_gui_integration.py # GUI集成测试
    └── unit/                      # 单元测试
        ├── test_api.py            # API单元测试
        ├── test_database.py       # 数据库单元测试
        ├── test_models.py         # 模型单元测试
        └── test_services.py       # 服务单元测试

```
