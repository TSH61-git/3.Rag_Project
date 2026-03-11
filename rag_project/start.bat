@echo off
echo ========================================
echo RAG Documentation Assistant
echo ========================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [3/4] Building index...
python build_index.py
if errorlevel 1 (
    echo ERROR: Failed to build index!
    pause
    exit /b 1
)

echo.
echo [4/4] Starting application...
echo.
echo ========================================
echo Application will start at:
echo http://127.0.0.1:7860
echo ========================================
echo.
python app.py
