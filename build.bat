@echo off

:: 清理旧构建
echo 清理旧构建文件...
call clean.bat

:: 安装构建依赖
echo 安装构建依赖...
pip install --upgrade build wheel

:: 执行构建
echo 开始构建应用包...
python -m build

:: 验证构建结果
if %errorlevel% equ 0 (
    echo 构建成功！生成文件:
    dir dist
) else (
    echo 构建失败，请检查错误信息
    exit /b 1
)