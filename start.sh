#!/bin/bash

cd Cafe_Three_Beavers

export PORT=5000
unset PIP_USER
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv --system-site-packages
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt || echo "Pip install failed, continuing..."
fi

echo "Starting application..."
python main.py