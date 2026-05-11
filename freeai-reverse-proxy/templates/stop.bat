@echo off
REM Stop the reverse proxy by killing whatever listens on 8888.
REM (Change the port number below if you used a non-default one.)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8888.*LISTENING"') do (
    echo Killing PID %%a ...
    taskkill /F /PID %%a
)
echo Done.
pause
