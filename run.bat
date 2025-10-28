@echo off
REM Credit Limit Assignment System - Quick Start Script for Windows

echo ==================================
echo Credit Limit Assignment System
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run setup if data doesn't exist
if not exist "data\credit_data.csv" (
    echo Running setup...
    python setup.py
) else (
    echo Data already exists, skipping setup...
)

REM Run Streamlit app
echo.
echo Starting Streamlit app...
echo Dashboard will open in your browser
echo.
streamlit run app.py

pause

