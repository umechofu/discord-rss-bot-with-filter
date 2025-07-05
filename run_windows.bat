@echo off
setlocal

REM Discord RSS Bot - Windows Execution Script

echo Starting Discord RSS Bot...

REM Move to script directory
cd /d "%~dp0"

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv --clear
    timeout /t 2 /nobreak >nul
    if not exist "venv\Scripts\python.exe" (
        echo Virtual environment creation failed, using system Python...
        goto skip_venv
    )
)

REM Activate virtual environment
echo Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
    set VENV_ACTIVE=1
) else (
    echo Warning: Virtual environment activation failed, using system Python...
    :skip_venv
    set VENV_ACTIVE=0
)

REM Install dependencies
echo Installing dependencies...
if %VENV_ACTIVE%==1 (
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install feedparser requests
) else (
    echo Using system Python installation...
    python -m pip install --user feedparser requests
)

REM Check configuration file
if not exist "config.json" (
    echo Error: config.json not found
    echo Please copy config.json.example to config.json and edit the configuration:
    echo copy config.json.example config.json
    pause
    exit /b 1
)

REM Run the bot
echo Starting Discord RSS Bot...
python rss_discord_bot.py

REM Deactivate virtual environment
if %VENV_ACTIVE%==1 (
    call venv\Scripts\deactivate.bat
)

pause