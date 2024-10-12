import os
import subprocess
import sys
import time
import platform

def custom_progress_bar(task_name, total_steps=10, step_duration=0.3):
    """
    Displays a simple progress bar using hash marks (#) to represent task progress.
    """
    print(f"{task_name}: [", end="", flush=True)
    for i in range(total_steps):
        print("#", end="", flush=True)
        time.sleep(step_duration)
    print("] Done!")

def loading_animation(message, duration=5):
    """
    Displays a loading animation with dots (...) for a specified duration.
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
        subprocess.check_call([sys.executable, "-m", "venv", "venv"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("Virtual environment already exists.")

def get_venv_executable(executable):
    """
    Returns the path to the executable within the virtual environment.
    """
    venv_path = os.path.join("venv", "Scripts" if platform.system() == "Windows" else "bin", executable)
    return venv_path

def install_dependencies():
    """
    Installs the required dependencies from the 'requirements.txt' file using pip.
    Suppresses the console log during the installation.
    """
    print("Installing dependencies...")
    custom_progress_bar("Setting up packages", total_steps=15, step_duration=0.2)
    pip_path = get_venv_executable("pip")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def install_pipreqs():
    """
    Installs the 'pipreqs' package, which is used to generate the 'requirements.txt' file.
    Suppresses the console log during installation.
    """
    loading_animation("Installing pipreqs (a tool to generate the requirements.txt)")
    pip_path = get_venv_executable("pip")
    subprocess.check_call([pip_path, "install", "pipreqs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def update_requirements():
    """
    Updates the 'requirements.txt' file using pipreqs, ensuring all installed
    packages are recorded. Suppresses the console log during the update.
    """
    loading_animation("Updating requirements.txt")
    pipreqs_path = get_venv_executable("pipreqs")
    subprocess.check_call([pipreqs_path, ".", "--force"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_application():
    """
    Runs the main application script 'main_assistant.py'.
    Displays a custom progress bar during the startup process.
    """
    print("Starting the application...\n")
    custom_progress_bar("Launching the Assistant", total_steps=10, step_duration=0.4)
    python_path = get_venv_executable("python")
    subprocess.call([python_path, "main_assistant.py"])

def main():
    """
    Main function that orchestrates the setup process for the Python Voice Assistant.
    It creates a virtual environment, installs dependencies, installs pipreqs, updates
    'requirements.txt', and runs the application.
    """
    print("\nWelcome to the Python Voice Assistant setup!")
    print("\nWe are setting up everything for you. Just follow the progress below!\n")
    
    create_virtual_env()
    install_dependencies()
    install_pipreqs()
    update_requirements()
    run_application()

if __name__ == "__main__":
    main()