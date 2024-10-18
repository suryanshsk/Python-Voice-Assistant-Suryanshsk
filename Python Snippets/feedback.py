import json
import os

FEEDBACK_FILE = "feedback.json"
feedback_list = []

def load_feedback():
    global feedback_list
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as file:
            feedback_list = json.load(file)
        print("Loaded your feedback.")
    else:
        print("No feedback to load.")

def save_feedback_to_file():
    with open(FEEDBACK_FILE, "w") as file:
        json.dump(feedback_list, file, indent=4)

def show_feedback():
    if feedback_list:
        print("Feedback Received:")
        for idx, feedback in enumerate(feedback_list, 1):
            print(f"{idx}. {feedback}")
    else:
        print("No feedback received yet!")

def submit_feedback():
    feedback = input("Enter your feedback (type 'exit' to stop): ")
    if feedback.lower() != 'exit':
        feedback_list.append(feedback)
        print("Thank you for your feedback!")
        save_feedback_to_file()

def clear_feedback():
    if feedback_list:
        feedback_list.clear()
        print("All feedback has been cleared.")
        save_feedback_to_file()
    else:
        print("No feedback to clear.")

def delete_feedback():
    show_feedback()
    if feedback_list:
        try:
            choice = int(input("Enter the number of the feedback you want to delete: ")) - 1
            if 0 <= choice < len(feedback_list):
                removed_feedback = feedback_list.pop(choice)
                print(f"Deleted feedback: {removed_feedback}")
                save_feedback_to_file()
            else:
                print("Invalid choice, no feedback deleted.")
        except ValueError:
            print("Please enter a valid number.")

def feedback_system():
    load_feedback()
    while True:
        print("\nFeedback System")
        print("1. Submit Feedback")
        print("2. Show Feedback")
        print("3. Clear All Feedback")
        print("4. Delete Feedback")
        print("5. Exit")

        choice = input("Please select an option (1-5): ")

        if choice == "1":
            submit_feedback()
        elif choice == "2":
            show_feedback()
        elif choice == "3":
            clear_feedback()
        elif choice == "4":
            delete_feedback()
        elif choice == "5":
            print("Exiting feedback system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    feedback_system()
