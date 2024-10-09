import os
import subprocess

def open_application(command):
    command = command.lower()  # Convert the command to lowercase for easier matching

    if 'calculator' in command:
        # For Windows
        subprocess.Popen('calc')  # Opens Calculator
        print("Opening Calculator...")

    elif 'notepad' in command:
        # For Windows
        subprocess.Popen('notepad')  # Opens Notepad
        print("Opening Notepad...")

    elif 'word' in command:
        # For Windows, adjust this command based on your installation
        subprocess.Popen('winword')  # Opens Microsoft Word
        print("Opening Microsoft Word...")

    elif 'excel' in command:
        # For Windows, adjust this command based on your installation
        subprocess.Popen('excel')  # Opens Microsoft Excel
        print("Opening Microsoft Excel...")

    else:
        print("Application not recognized. Please try again.")
