@echo off

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate

:: Check if the activation was successful
if "%VIRTUAL_ENV%" NEQ "" (
    echo Virtual environment activated.

    :: Install the required packages
    pip install progressbar2 colorama
    :: Run the main application
    python setup.py
) else (
    echo Failed to activate virtual environment.
)