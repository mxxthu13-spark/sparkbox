@echo off
chcp 65001 >nul
echo ========================================
echo SparkBox v1.0 备份工具
echo ========================================
echo.

set BACKUP_DIR=sparkbox_v1.0_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%

echo 创建备份目录: %BACKUP_DIR%
mkdir "%BACKUP_DIR%"

echo.
echo [1/8] 备份后端代码...
xcopy /E /I /Y backend "%BACKUP_DIR%\backend" >nul
echo ✓ 后端代码备份完成

echo.
echo [2/8] 备份前端代码...
xcopy /E /I /Y frontend "%BACKUP_DIR%\frontend" >nul
echo ✓ 前端代码备份完成

echo.
echo [3/8] 备份文档...
xcopy /E /I /Y docs "%BACKUP_DIR%\docs" >nul
echo ✓ 文档备份完成

echo.
echo [4/8] 备份根目录文件...
copy README.md "%BACKUP_DIR%\" >nul
copy FINAL_COMPLETE.md "%BACKUP_DIR%\" >nul 2>nul
copy COMPLETE.md "%BACKUP_DIR%\" >nul 2>nul
echo ✓ 根目录文件备份完成

echo.
echo [5/8] 备份数据库...
if exist backend\sparkbox.db (
    copy backend\sparkbox.db "%BACKUP_DIR%\sparkbox.db" >nul
    echo ✓ 数据库备份完成
) else (
    echo ⚠ 未找到数据库文件
)

echo.
echo [6/8] 清理临时文件...
rd /s /q "%BACKUP_DIR%\backend\venv" 2>nul
rd /s /q "%BACKUP_DIR%\backend\__pycache__" 2>nul
rd /s /q "%BACKUP_DIR%\frontend\node_modules" 2>nul
rd /s /q "%BACKUP_DIR%\frontend\dist" 2>nul
del /s /q "%BACKUP_DIR%\*.pyc" 2>nul
echo ✓ 临时文件清理完成

echo.
echo [7/8] 创建版本信息...
(
echo SparkBox v1.0 备份
echo.
echo 备份时间: %date% %time%
echo 备份内容:
echo - 后端代码 ^(backend/^)
echo - 前端代码 ^(frontend/^)
echo - 文档 ^(docs/^)
echo - 数据库 ^(sparkbox.db^)
echo - README.md
echo.
echo 恢复说明:
echo 1. 解压备份文件
echo 2. 安装后端依赖: cd backend ^&^& pip install -r requirements.txt
echo 3. 安装前端依赖: cd frontend ^&^& npm install
echo 4. 配置 .env 文件
echo 5. 启动服务
echo.
echo 注意事项:
echo - 请妥善保管 .env 文件中的密钥
echo - 数据库文件包含所有用户数据
echo - 定期备份以防数据丢失
) > "%BACKUP_DIR%\VERSION.txt"
echo ✓ 版本信息创建完成

echo.
echo [8/8] 压缩备份文件...
powershell -command "Compress-Archive -Path '%BACKUP_DIR%' -DestinationPath '%BACKUP_DIR%.zip' -Force"
if exist "%BACKUP_DIR%.zip" (
    echo ✓ 备份文件压缩完成
    rd /s /q "%BACKUP_DIR%"
    echo.
    echo ========================================
    echo 备份完成！
    echo ========================================
    echo.
    echo 备份文件: %BACKUP_DIR%.zip
    echo 文件大小: 
    dir "%BACKUP_DIR%.zip" | findstr ".zip"
    echo.
) else (
    echo ✗ 压缩失败，保留未压缩的备份目录
    echo 备份目录: %BACKUP_DIR%
)

echo.
echo 按任意键退出...
pause >nul
