@echo off
setlocal
echo Starting services...

REM === Step 1: Check PostgreSQL database connections ===
echo Checking PostgreSQL connections...

psql -U postgres -d user_db -c "\q"
IF %ERRORLEVEL% NEQ 0 (
  echo Cannot connect to user_db!
) ELSE (
  echo Connected to user_db successfully.
)

psql -U postgres -d task_db -c "\q"
IF %ERRORLEVEL% NEQ 0 (
  echo Cannot connect to task_db!
) ELSE (
  echo Connected to task_db successfully.
)

REM === Step 2: Launch FastAPI backend services (minimized with logs) ===
echo Launching FastAPI services...

start "" /min cmd /c "set DATABASE_URL=postgresql://todo:123456@localhost:5432/user_db && python -m uvicorn user_service.app:app --reload --host 0.0.0.0 --port 8000 > user_log.txt 2>&1"
start "" /min cmd /c "set DATABASE_URL=postgresql://todo:123456@localhost:5432/task_db && set USER_SERVICE_URL=http://192.168.1.158:8000 && python -m uvicorn task_service.app:app --reload --host 0.0.0.0 --port 8001 > task_log.txt 2>&1"

REM === Step 3: Automatically open frontend index.html ===
echo Opening frontend page...
start "" "static/index.html"

REM === Step 4: Show popup message for success ===
powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Backend services started and frontend opened successfully!','Task Management System')"

exit /b

