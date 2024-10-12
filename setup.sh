#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Check if the activation was successful
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "Virtual environment activated."
    
    # Run the main application
    python setup.py
else
    echo "Failed to activate virtual environment."
fi