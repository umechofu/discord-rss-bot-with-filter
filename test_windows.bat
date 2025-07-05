@echo off
setlocal

REM Discord RSS Bot - Windows Test Execution Script

echo Running Discord RSS Bot test...

REM Move to script directory
cd /d "%~dp0"

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
python -m pip install feedparser requests

REM Check configuration file
if not exist "config.json" (
    echo Error: config.json not found
    echo Please copy config.json.example to config.json and edit the configuration:
    echo copy config.json.example config.json
    pause
    exit /b 1
)

REM Run the bot in test mode (once only)
echo Running Discord RSS Bot in test mode (once only)...
python rss_discord_bot.py --once

echo Test execution completed.

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause