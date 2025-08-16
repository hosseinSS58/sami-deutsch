@echo off
chcp 65001 >nul
title Sami Deutsch - Network Server Runner

echo.
echo 🌐 Sami Deutsch - Network Server Runner
echo ==================================================
echo.

REM Check if manage.py exists
if not exist "manage.py" (
    echo ❌ Error: manage.py not found. Please run this script from the Django project root.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if Django is installed
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Django not found. Please install Django first.
    pause
    exit /b 1
)

echo ✅ Django project found
echo ✅ Python environment ready
echo.

REM Get server configuration
echo 📋 Server Configuration:
echo 1. Local only (localhost:8000)
echo 2. Network access (0.0.0.0:8000)
echo 3. Custom configuration
echo.

set /p choice="Select option (1-3): "

if "%choice%"=="1" (
    set host=127.0.0.1
    set port=8000
    echo.
    echo 🚀 Starting local server...
    echo 📍 Access: http://localhost:8000
) else if "%choice%"=="2" (
    set host=0.0.0.0
    set port=8000
    echo.
    echo 🚀 Starting network server...
    echo 📍 Local access: http://localhost:8000
    echo 🌐 Network access: http://%COMPUTERNAME%:8000
    echo 🔧 Server binding: 0.0.0.0:8000
) else if "%choice%"=="3" (
    set /p host="Enter host (default: 0.0.0.0): "
    if "%host%"=="" set host=0.0.0.0
    
    set /p port_input="Enter port (default: 8000): "
    if "%port_input%"=="" set port_input=8000
    
    set port=%port_input%
    echo.
    echo 🚀 Starting custom server...
    echo 🔧 Server binding: %host%:%port%
) else (
    echo ❌ Invalid choice. Using default network configuration.
    set host=0.0.0.0
    set port=8000
    echo.
    echo 🚀 Starting network server...
)

echo.
echo ⏹️  Press Ctrl+C to stop the server
echo.

REM Run migrations
echo 🔄 Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ⚠️  Warning: Migrations failed, but continuing...
) else (
    echo ✅ Migrations completed successfully
)

echo.

REM Collect static files
echo 🔄 Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo ⚠️  Warning: Static files collection failed, but continuing...
) else (
    echo ✅ Static files collected successfully
)

echo.

REM Start Django server
echo 🚀 Starting Django server...
python manage.py runserver %host%:%port%

echo.
echo 🛑 Server stopped
pause
