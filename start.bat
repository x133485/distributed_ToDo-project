@echo off
setlocal
echo Starting services...

REM === Step 1: 检查数据库连接 ===
echo Checking PostgreSQL connections...

psql -U postgres -d user_db -c "\q"
IF %ERRORLEVEL% NEQ 0 (
  echo  Cannot connect to user_db!
) ELSE (
  echo Connected to user_db.
)

psql -U postgres -d task_db -c "\q"
IF %ERRORLEVEL% NEQ 0 (
  echo  Cannot connect to task_db!
) ELSE (
  echo Connected to task_db.
)

REM === Step 2: 启动 FastAPI 服务（最小化 + 日志） ===
echo Launching FastAPI services...

start "" /min cmd /c "python -m uvicorn user_service.app:app --reload --port 8000> user_log.txt 2>&1"
start "" /min cmd /c "python -m uvicorn task_service.app:app --reload --port 8001 > task_log.txt 2>&1"

REM === Step 3: 弹窗通知成功 ===
powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Services started successfully!','Task System')"

