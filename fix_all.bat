@echo off
echo ============================================================
echo SparkBox Fix Tool
echo ============================================================
echo.

cd /d "%~dp0backend"

echo [1/5] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found
    echo Please run: python -m venv venv
    pause
    exit /b 1
)
echo OK: Virtual environment exists

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo OK: Virtual environment activated

echo.
echo [3/5] Checking database...
if not exist "sparkbox.db" (
    echo ERROR: Database file not found
    pause
    exit /b 1
)
echo OK: Database file exists

echo.
echo [4/5] Fixing database structure and data...
python fix_reviews_data.py
if errorlevel 1 (
    echo ERROR: Database fix failed
    pause
    exit /b 1
)

echo.
echo [5/5] Checking latest thought time...
python -c "from sqlalchemy import create_engine, text; from core.config import settings; engine = create_engine(settings.DATABASE_URL.replace('+aiosqlite', '')); conn = engine.connect(); result = conn.execute(text('SELECT content, created_at FROM thoughts WHERE is_deleted = 0 ORDER BY created_at DESC LIMIT 1')); row = result.fetchone(); print(f'\nLatest thought: {row[0][:50]}...' if row else '\nNo thoughts'); print(f'Created at: {row[1]}' if row else ''); conn.close()"

echo.
echo ============================================================
echo Fix completed!
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. Restart backend server
echo    - If backend is running, press Ctrl+C to stop
echo    - Run: python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 2. Clear browser cache
echo    - Press Ctrl+Shift+R multiple times
echo    - Or press F12, type: localStorage.clear()
echo.
echo 3. Test features
echo    - Create new thought, check time display
echo    - Select category, check statistics
echo    - View review details
echo.
pause
