#!/bin/bash
# Quick Start Script for Linux/Mac

echo "===================================="
echo "FastAPI Template - Quick Start"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/5] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
    echo "Please edit .env file with your configuration"
else
    echo ".env file already exists"
fi

echo "[5/5] Initializing database..."
python -m app.db.init_db

echo ""
echo "===================================="
echo "Setup completed successfully!"
echo "===================================="
echo ""
echo "To start the server, run:"
echo "   python run.py"
echo ""
echo "Or use:"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "API will be available at:"
echo "   - http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo ""
