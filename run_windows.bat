@echo off
setlocal

REM Discord RSS Bot - Windows Execution Script

echo Starting Discord RSS Bot...

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

REM Run the bot
echo Starting Discord RSS Bot...
python rss_discord_bot.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause