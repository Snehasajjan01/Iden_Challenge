@echo off
echo ========================================
echo    Product Dashboard Launcher
echo ========================================
echo.

echo Step 1: Installing Flask...
pip install Flask --user

echo.
echo Step 2: Starting Dashboard...
echo.
echo The dashboard will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python simple_app.py

pause
