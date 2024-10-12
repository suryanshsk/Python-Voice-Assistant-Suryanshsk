import time
import sys
import progressbar
from colorama import Style,Fore


def custom_progress_bar(task_name, total_steps, step_duration, color):
    """
    Displays a colored progress bar using progressbar with a customizable number of total steps and step duration.
    """
    colored_task_name = f"{color}{task_name}{Style.RESET_ALL}"

    # Initialize the progress bar with solid blocks
    bar = progressbar.ProgressBar(max_value=total_steps, widgets=[
        colored_task_name,
        ' ', progressbar.Percentage(),
        ' ', progressbar.Bar('█', '░'),  # Use solid blocks for the filled part and light blocks for the empty part
        ' ', progressbar.ETA(),

    ]).start()

    for i in range(total_steps):
        time.sleep(step_duration)  # Simulate work being done
        bar.update(i + 1)  # Update the progress bar

def loading_spinner(duration, color, message):
    """
    Displays a spinner without a progress bar, using only the spinner symbols and message.
    """
    spinner = ['-', '\\', '|', '/']
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in spinner:
            sys.stdout.write(f'\r{color}{message} {frame} {Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write(f'\n')
    sys.stdout.flush()
