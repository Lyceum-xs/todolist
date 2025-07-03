from setuptools import setup, find_packages

setup(
    name='ToDo-List',
    version='0.1.0',
    author="这对吗这不队",
    description="A modern To-Do List application with task management, habit tracking, and productivity tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://whucsgitlab.whu.edu.cn/devops/todolist.git",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.0",
        "pydantic>=1.8.0",
        "python-dotenv>=0.19.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'todo-list = run:main',
        ],
    },
    scripts=['run.py'],
)