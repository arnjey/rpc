@echo off
REM Start ValoRPC API Server (Windows)
REM Run this to start the web dashboard on localhost:8000

echo.
echo 🎮 Starting ValoRPC API Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask not found, installing dependencies...
    pip install -r requirements.txt
)

echo ✅ Starting server on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the API server
python api_server.py

pause
