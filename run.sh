#!/bin/bash

# Credit Limit Assignment System - Quick Start Script

echo "=================================="
echo "Credit Limit Assignment System"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run setup if data doesn't exist
if [ ! -f "data/credit_data.csv" ]; then
    echo "Running setup..."
    python setup.py
else
    echo "Data already exists, skipping setup..."
fi

# Run Streamlit app
echo ""
echo "Starting Streamlit app..."
echo "Dashboard will open in your browser"
echo ""
streamlit run app.py

