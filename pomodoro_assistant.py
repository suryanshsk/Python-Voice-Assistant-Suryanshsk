import time
import json
import matplotlib.pyplot as plt

# File names for storing user data and Pomodoro history
USER_FILE = "user_data.json"
HISTORY_FILE = "pomodoro_history.json"

# Load user data from a JSON file, or return an empty dictionary if the file is not found
def load_user_data():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user details to a JSON file
def save_user_details(data):
    with open(USER_FILE, "w") as file:
        json.dump(data, file)

# Register a new user with a username and password
def register_user(username, password):
    users = load_user_data()
    if username in users:
        return False  # User already exists
    users[username] = password
    save_user_details(users)
    return True

# Authenticate a user based on username and password
def authenticate_user(username, password):
    users = load_user_data()
    return users.get(username) == password

# Save a Pomodoro session to history JSON file
def save_history(pomodoro):
    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    history.append(pomodoro)
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

# Load Pomodoro session history from JSON file
def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Run the Pomodoro timer with specified work, break durations, and cycles
def pomodoro_timer(work_duration=25, break_duration=5, cycles=4):
    for cycle in range(cycles):
        task = input(f"Enter task for Pomodoro #{cycle + 1}: ")
        print(f"Starting Pomodoro #{cycle + 1}. Work for {work_duration} minutes.")
        time.sleep(work_duration * 60)  # Simulate timer

        # Save work period to history
        save_history({"task": task, "type": "work", "cycle": cycle + 1})

        # Break period after each work session, except the last one
        if cycle < cycles - 1:
            print(f"Time for a break! Relax for {break_duration} minutes.")
            time.sleep(break_duration * 60)
            save_history({"task": task, "type": "break", "cycle": cycle + 1})

    print("Congratulations! You've completed your Pomodoros.")
    display_progress()

# Display a summary of Pomodoro progress using matplotlib
def display_progress():
    history = load_history()
    work_count = sum(1 for h in history if h['type'] == 'work')
    break_count = sum(1 for h in history if h['type'] == 'break')
    print(f"Total Work Sessions: {work_count}")
    print(f"Total Breaks: {break_count}")

    # Generate a bar chart for summary
    plt.bar(['Work Sessions', 'Breaks'], [work_count, break_count])
    plt.title('Pomodoro Progress Summary')
    plt.xlabel('Session Type')
    plt.ylabel('Count')
    plt.show()

# Main function for user registration, login, and Pomodoro timer functionality
def main():
    # User Authentication
    while True:
        action = input("Do you want to register (r) or log in (l)? ").strip().lower()
        if action in ('r', 'l'):
            username = input("Enter username: ")
            password = input("Enter password: ")

            if action == 'r':
                if register_user(username, password):
                    print("Registration successful.")
                else:
                    print("Username already exists.")
            elif action == 'l':
                if authenticate_user(username, password):
                    print("Login successful.")
                    break
                else:
                    print("Invalid username or password.")
        else:
            print("Invalid action.")

    # Start Pomodoro Timer
    while True:
        command = input("Enter 'start' to begin the Pomodoro timer, 'exit' to quit: ").strip().lower()

        if command == "start":
            work_time = int(input("Enter work duration in minutes (default 25): ") or 25)
            break_time = int(input("Enter break duration in minutes (default 5): ") or 5)
            cycles = int(input("Enter number of cycles (default 4): ") or 4)

            # Start timer with pause/resume functionality
            paused = False
            for cycle in range(cycles):
                if paused:
                    print("Pomodoro is paused. Type 'resume' to continue or 'exit' to quit.")
                    command = input().strip().lower()
                    if command == "resume":
                        paused = False
                    elif command == "exit":
                        print("Exiting Pomodoro timer.")
                        return

                # Work Period
                task = input(f"Enter task for Pomodoro #{cycle + 1}: ")
                print(f"Starting Pomodoro #{cycle + 1}. Work for {work_time} minutes.")
                time.sleep(work_time * 60)

                # Save work session to history
                save_history({"task": task, "type": "work", "cycle": cycle + 1})

                # Break Period
                if cycle < cycles - 1:
                    print(f"Time for a break! Relax for {break_time} minutes.")
                    time.sleep(break_time * 60)
                    save_history({"task": task, "type": "break", "cycle": cycle + 1})

            print("Congratulations! You've completed your Pomodoros.")
            display_progress()

        elif command == "exit":
            print("Exiting Pomodoro timer.")
            break
        else:
            print("Invalid command. Please enter 'start' or 'exit'.")

if __name__ == "__main__":
    main()
