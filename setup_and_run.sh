#!/bin/bash

# Clone repository using SHH if it is not already cloned
if [ ! -d "alphaby_market_scrapper" ]; then
    echo "Cloning repository using SSH..."
    git clone git@github.com:Lorenabd/alphaby_market_scrapper.git
fi

# Change to repository directory
cd alphaby_market_scrapper

# Create and activate a virtual environment (optional)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate  # On Linux/macOS

echo "Installing dependencies from requirements.txt..."
pip install --timeout=300 -r requirements.txt

# Source the environment variables from env.sh
echo "Setting environment variables from env.sh..."
source env.sh 

# Ejecutar el script dentro del repositorio
echo "Executing script..."
python access_market.py
