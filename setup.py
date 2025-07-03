from setuptools import setup, find_packages

setup(
    name='ToDo-List',
    version='0.1.0',
    author="这对吗这不队",
    description="A short description",
    long_description = open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://whucsgitlab.whu.edu.cn/devops/todolist.git",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)