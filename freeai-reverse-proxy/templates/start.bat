@echo off
REM Launch the reverse proxy on http://127.0.0.1:8888
REM Double-click to run; closes when you close the console window.

cd /d "%~dp0"
echo Starting reverse proxy on http://127.0.0.1:8888 ...
echo Press Ctrl+C to stop.
echo.
python run.py
pause
