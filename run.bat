@echo off
echo ========================================
echo   InterviewAI - Starting Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed!
)

echo.
echo [2/3] Checking .env file...
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create .env file with your GROQ_API_KEY
    echo Example: GROQ_API_KEY=your_key_here
    echo.
    pause
)

echo.
echo [3/3] Starting InterviewAI...
echo.
echo ========================================
echo   Application will open in browser
echo   URL: http://localhost:8501
echo   Press Ctrl+C to stop
echo ========================================
echo.

python -m streamlit run ui/app.py

pause
