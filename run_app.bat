@echo off
echo Starting Product Dashboard...
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask application...
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
