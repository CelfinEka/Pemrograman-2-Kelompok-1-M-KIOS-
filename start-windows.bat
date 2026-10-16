@echo off
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (echo Python tidak ditemukan. Install Python dan tambahkan ke PATH.& pause& exit /b 1)
if not exist .venv\Scripts\python.exe (python -m venv .venv || exit /b 1)
.venv\Scripts\python.exe -m pip install -r requirements.txt || exit /b 1
.venv\Scripts\python.exe manage.py migrate || exit /b 1
echo.
echo BUKA http://127.0.0.1:8000
.venv\Scripts\python.exe manage.py runserver
pause
