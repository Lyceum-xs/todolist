from setuptools import setup, find_packages
import os

# 读取README内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 获取依赖列表
def get_requirements():
    with open("requirements.txt", "r", encoding='utf-8') as f:
        return f.read().splitlines()

# 强制设置包名和版本
PACKAGE_NAME = "todolist_app"
PACKAGE_VERSION = "1.0.0"

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="这对吗这不队",
    author_email="your.email@example.com",  # 添加邮箱
    description="Modern To-Do List application with task management and productivity tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://whucsgitlab.whu.edu.cn/devops/todolist.git",
    
    # 包配置
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    
    # 包含数据文件
    include_package_data=True,
    package_data={
        '': ['*.yaml', '*.ini'],  # 包含配置文件
        'app': ['templates/*', 'static/*'],  # 包含前端资源
    },
    
    # 依赖管理
    install_requires=get_requirements(),
    
    # 开发依赖
    extras_require={
        'dev': [
            'pytest>=6.0',
            'coverage',
            'flake8'
        ]
    },
    
    # 分类信息
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
    ],
    
    python_requires=">=3.8",
    
    # 入口点配置 - 确保格式正确
    entry_points={
        'console_scripts': [
            'todo-list=run:main',  # 指向run.py的main函数
        ],
    },
    
    # 其他元数据
    keywords='todo task productivity',
    project_urls={
        "Source Code": "https://whucsgitlab.whu.edu.cn/devops/todolist.git",
        "Bug Tracker": "https://whucsgitlab.whu.edu.cn/devops/todolist/-/issues",
    },
    license='MIT',
    
    # 确保资源文件正确包含
    zip_safe=False,
    
    # 明确包含run.py模块
    py_modules=['run'],
    
    # 强制设置分发名称
    options={
        'bdist_wheel': {
            'dist_name': PACKAGE_NAME,
            'universal': True
        },
        'sdist': {
            'dist_name': PACKAGE_NAME
        }
    }
)