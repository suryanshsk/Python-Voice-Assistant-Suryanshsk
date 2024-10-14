#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Check if the activation was successful
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "Virtual environment activated."
    pip install progressbar2 colorama
    # Run the main application
    python cli_setup.py
else
    echo "Failed to activate virtual environment."
fi