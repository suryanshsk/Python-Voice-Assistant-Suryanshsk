import os
import subprocess
import sys
import time

def custom_progress_bar(task_name, total_steps=10, step_duration=0.3):
    """
    Displays a simple progress bar using hash marks (#) to represent task progress.

    Args:
        task_name (str): Name of the task to be displayed before the progress bar.
        total_steps (int): Total number of steps for the progress bar. Default is 10.
        step_duration (float): Duration of each step in seconds. Default is 0.3 seconds.
    """
    print(f"{task_name}: [", end="", flush=True)
    for i in range(total_steps):
        print("#", end="", flush=True)
        time.sleep(step_duration)
    print("] Done!")

def loading_animation(message, duration=5):
    """
    Displays a loading animation with dots (...) for a specified duration.

    Args:
        message (str): Message to display before the loading animation.
        duration (int): Duration for how long the animation should run. Default is 5 seconds.
    """
    print(message, end="", flush=True)
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(" Done!")

def create_virtual_env():
    """
    Creates a virtual environment named 'venv' in the current directory, 
    if it does not already exist. Displays an animation while creating.
    """
    if not os.path.exists('venv'):
        loading_animation("Creating virtual environment")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    """
    Installs the required dependencies from the 'requirements.txt' file
    using pip. Displays a custom progress bar during the installation process.
    """
    print("Installing dependencies...")
    custom_progress_bar("Setting up packages", total_steps=15, step_duration=0.2)
    subprocess.check_call([os.path.join("venv", "bin", "pip"), "install", "-r", "requirements.txt"])

def install_pipreqs():
    """
    Installs the 'pipreqs' package, which is used to generate the 'requirements.txt' file.
    Displays an animation during installation.
    """
    loading_animation("Installing pipreqs (a tool to generate the requirements.txt)")
    subprocess.check_call([os.path.join("venv", "bin", "pip"), "install", "pipreqs"])

def update_requirements():
    """
    Updates the 'requirements.txt' file using pipreqs, ensuring all installed
    packages are recorded. Displays an animation during the update process.
    """
    loading_animation("Updating requirements.txt")
    subprocess.check_call([os.path.join("venv", "bin", "pipreqs"), ".", "--force"])

def run_application():
    """
    Runs the main application script 'main_assistant.py'. 
    Displays a custom progress bar during the startup process.
    """
    print("Starting the application...\n")
    custom_progress_bar("Launching the Assistant", total_steps=10, step_duration=0.4)
    subprocess.call([os.path.join("venv", "bin", "python"), "main_assistant.py"])

def main():
    """
    Main function that orchestrates the setup process for the Python Voice Assistant.
    It creates a virtual environment, installs dependencies, installs pipreqs, updates
    'requirements.txt', and runs the application.
    """
    print("\nWelcome to the Python Voice Assistant setup! We are setting up everything for you.")
    print("No coding knowledge needed. Just follow the progress below!\n")
    
    create_virtual_env()
    install_dependencies()
    install_pipreqs()
    update_requirements()
    run_application()

if __name__ == "__main__":
    main()
