from setuptools import setup, find_packages
import os

# 读取README内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 获取依赖列表
def get_requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()

setup(
    name='todo-list-app',
    version='0.1.1',
    author="这对吗这不队",
    description="Modern To-Do List application with task management and productivity tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://whucsgitlab.whu.edu.cn/devops/todolist.git",
    
    # 正确配置包目录
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
    
    # 入口点配置
    entry_points={
        'console_scripts': [
            'todo-list=run:main',  # 指向run.py的main函数
        ],
    },
    
    # 添加其他元数据
    keywords='todo task productivity',
    project_urls={
        "Source Code": "https://whucsgitlab.whu.edu.cn/devops/todolist.git",
        "Bug Tracker": "https://whucsgitlab.whu.edu.cn/devops/todolist/-/issues",
    },
    
    # 添加许可证信息
    license='MIT',
    
    # 添加命令行脚本
    scripts=['run.py'],
    
    # 设置zip_safe为False以确保资源文件正确加载
    zip_safe=False
)