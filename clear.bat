@echo off
echo 开始清理项目...

:: 删除构建产物
rmdir /s /q build
rmdir /s /q dist
del /q src\*.egg-info 2>nul

:: 删除Python缓存
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul

:: 删除测试缓存
rmdir /s /q .pytest_cache 2>nul
del /q .coverage 2>nul
rmdir /s /q htmlcov 2>nul

echo 清理完成！项目已回到干净状态