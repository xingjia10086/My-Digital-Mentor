@echo off
setlocal
echo Setting up Daily Push...

set TASK_NAME="Xingjia_Daily_Inspiration_Push"
set PROG_DIR=%~dp0
set SCRIPT_NAME=daily_push.py

schtasks /delete /tn %TASK_NAME% /f >nul 2>&1

set VBS_SCRIPT=%PROG_DIR%run_hidden.vbs
echo CreateObject("WScript.Shell").Run "cmd /c cd /d """ ^& "%PROG_DIR%" ^& """ & python """ ^& "%SCRIPT_NAME%" ^& """", 0, False > "%VBS_SCRIPT%"

schtasks /create /tn %TASK_NAME% /tr "wscript.exe \"%VBS_SCRIPT%\"" /sc daily /st 09:00 /f

if %errorlevel% == 0 (
    echo SUCCESS: Scheduled task created for 09:00 AM daily.
) else (
    echo ERROR: Failed to create scheduled task.
)

