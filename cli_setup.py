import os
import subprocess
import sys
import platform
from utils.loader import custom_progress_bar, loading_spinner
from colorama import init, Fore, Style
from utils.cli.cli_art import display_art

# Initialize colorama for colored console output
init(autoreset=True)

def get_venv_executable(executable):
    """
    Returns the path to the executable within the virtual environment.
    """
    venv_path = os.path.join("venv", "Scripts" if platform.system() == "Windows" else "bin", executable)
    return venv_path

def install_dependencies():
    """
    Installs the required dependencies from the 'requirements.txt' file using pip.
    Displays a progress bar and a success/failure message after installation.
    """
    task_name = "Installing dependencies"
    total_steps = 500
    step_duration = 0.02

    custom_progress_bar(task_name, total_steps, step_duration, color=Fore.GREEN)
    
    pip_path = get_venv_executable("pip")
    try:
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        print(f"\n{Fore.GREEN}✓ Successfully installed dependencies!{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"\n{Fore.RED}✗ Failed to install dependencies!{Style.RESET_ALL}")
        sys.exit(1)

def install_pipreqs():
    """
    Installs the 'pipreqs' package, which is used to generate the 'requirements.txt' file.
    Displays a progress bar and a success/failure message after installation.
    """
    task_name = "Installing pipreqs (tool for generating requirements.txt)"
    total_steps = 500
    step_duration = 0.02

    custom_progress_bar(task_name, total_steps, step_duration, color=Fore.YELLOW)
    
    pip_path = get_venv_executable("pip")
    try:
        subprocess.check_call([pip_path, "install", "pipreqs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"\n{Fore.GREEN}✓ Successfully installed pipreqs!{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"\n{Fore.RED}✗ Failed to install pipreqs!{Style.RESET_ALL}")
        sys.exit(1)

def update_requirements():
    """
    Updates the 'requirements.txt' file using pipreqs, ensuring all installed
    packages are recorded. Displays a progress bar and a success/failure message.
    """
    task_name = "Updating requirements.txt"
    total_steps = 500
    step_duration = 0.02

    custom_progress_bar(task_name, total_steps, step_duration, color=Fore.YELLOW)
    
    pipreqs_path = get_venv_executable("pipreqs")
    try:
        subprocess.check_call([pipreqs_path, ".", "--force"])
        print(f"\n{Fore.GREEN}✓ Successfully updated requirements.txt!{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"\n{Fore.RED}✗ Failed to update requirements.txt!{Style.RESET_ALL}")
        sys.exit(1)

def run_application():
    """
    Runs the main application script 'main_assistant.py'.
    Displays a progress bar during the startup process and a success/failure message after.
    """
    task_name = "Launching the Assistant"
    total_steps = 500
    step_duration = 0.05

    custom_progress_bar(task_name, total_steps, step_duration, color=Fore.CYAN)
    
    python_path = get_venv_executable("python")
    try:
        subprocess.call([python_path, "main_assistant.py"])
        print(f"{Fore.GREEN}✓ Assistant launched successfully!{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}✗ Failed to launch the assistant!{Style.RESET_ALL}")
        sys.exit(1)

def main():
    """
    Main function that orchestrates the setup process for the Python Voice Assistant.
    It installs dependencies, installs pipreqs, updates 'requirements.txt', and runs the application.
    """
    print("\nWelcome to the Python Voice Assistant setup! We are setting up everything for you.")
    print("No coding knowledge needed. Just follow the progress below!\n")
    
    display_art()
    # Use loading spinner for initialization
    loading_spinner(2, Fore.CYAN, "Initializing setup environment...")
    # update_requirements()
    install_dependencies()
    install_pipreqs()
    # update_requirements()
    run_application()

if __name__ == "__main__":
    main()
