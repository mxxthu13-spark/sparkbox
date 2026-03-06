@echo off
chcp 65001 >nul
echo ========================================
echo SparkBox 一键修复脚本
echo ========================================
echo.

echo [1/5] 运行数据库迁移...
cd /d d:\Cursor\sparkbox\backend
python migrate_reviews.py
if errorlevel 1 (
    echo 错误：数据库迁移失败！
    pause
    exit /b 1
)
echo.

echo [2/5] 测试数据库...
python test_reviews.py
echo.

echo [3/5] 检查后端文件...
if not exist "main.py" (
    echo 错误：找不到 main.py
    pause
    exit /b 1
)
echo 后端文件检查通过
echo.

echo [4/5] 准备重启后端...
echo 请手动执行以下步骤：
echo.
echo 1. 找到运行后端的终端窗口
echo 2. 按 Ctrl+C 停止后端
echo 3. 运行以下命令：
echo.
echo    cd d:\Cursor\sparkbox\backend
echo    venv\Scripts\activate
echo    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.

echo [5/5] 前端修复提示...
echo.
echo 打开浏览器后，请执行：
echo 1. 按 Ctrl+Shift+R 强制刷新（多按几次）
echo 2. 按 F12 打开控制台
echo 3. 在 Console 中输入：localStorage.clear()
echo 4. 再次刷新页面
echo.

echo ========================================
echo 修复脚本执行完成！
echo ========================================
echo.
echo 接下来请按照 COMPLETE_FIX_GUIDE.md 中的步骤测试
echo.
pause
