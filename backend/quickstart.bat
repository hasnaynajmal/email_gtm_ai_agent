@echo off
REM Quick Start Script for Windows

echo ====================================
echo FastAPI Template - Quick Start
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example
    echo Please edit .env file with your configuration
) else (
    echo .env file already exists
)

echo [5/5] Initializing database...
python -m app.db.init_db

echo.
echo ====================================
echo Setup completed successfully!
echo ====================================
echo.
echo To start the server, run:
echo    python run.py
echo.
echo Or use:
echo    venv\Scripts\activate
echo    python run.py
echo.
echo API will be available at:
echo    - http://localhost:8000
echo    - Docs: http://localhost:8000/docs
echo.

pause
