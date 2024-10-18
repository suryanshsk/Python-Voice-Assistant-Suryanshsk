from gemini_info import get_gemini_response
import re
from datetime import datetime

def extract_reminder(input_text):
    template = f"""I will provide a natural language text that contains a reminder request and today is {datetime.today()}. Your task is to extract two main components from it:

        Reminder Message: What the user wants to be reminded about.
        Reminder Time: Carefuly return the specific date and time carefully when the user wants to be reminded, formatted as an ISO 8601 date-time string (YYYY-MM-DDTHH:MM:SS).

    For any unclear or ambiguous time references (like "next Monday" or "tomorrow"), convert them to a specific date and time. Use the following rules:

        If the time is not specified, default to 9:00 AM on that day.
        Handle common terms like "morning," "afternoon," and "evening" as 9:00 AM, 3:00 PM, and 7:00 PM, respectively.
        If no time-related information is provided, assume the user means today at the next available hour.

    Return the output as a structured JSON object with the fields reminder_message and reminder_time.

    Here are some examples:

    Example 1:

        Input: "Remind me to go shopping tomorrow at 5pm."
        Output:

        json

        
        "reminder_message": "go shopping",
        "reminder_time": "2024-10-07T17:00:00"
        

    Example 2:

        Input: "Let's meet next Friday morning."
        Output:

        json

        
        "reminder_message": "meet",
        "reminder_time": "2024-10-11T09:00:00"
        

    Example 3:

        Input: "The meeting is in 2 hours."
        Output:

        json

        
        "reminder_message": "meeting",
        "reminder_time": "2024-10-06T14:00:00"
    Example 4:

        Input: "Remind me to send the report on October 20th."
        Output:

        json

        
        "reminder_message": "send the report",
        "reminder_time": "2024-10-20T09:00:00"
        

    Your turn:

        Input: "{input_text}"""
    

    api_response = get_gemini_response(template)
    # Regular expressions to extract reminder_message and reminder_time
    message_pattern = r'"reminder_message":\s*"([^"]+)"'
    time_pattern = r'"reminder_time":\s*"([^"]+)"'

    # Extracting the reminder message
    message_match = re.search(message_pattern, api_response)
    reminder_message = message_match.group(1) if message_match else None

    # Extracting the reminder time
    time_match = re.search(time_pattern, api_response)
    reminder_time = time_match.group(1) if time_match else None

    # # Output the extracted values
    # print(f"Reminder Message: {reminder_message}")
    # print(f"Reminder Time: {reminder_time}")

    rem_time, message = reminder_time, reminder_message
    print(rem_time, message)
    reminder_dt = datetime.fromisoformat(rem_time)
    from main_assistant import REMINDERS
    # Check if the reminder time is in the past
    if reminder_dt < datetime.now():
        print("The reminder time is in the past. Please set a future reminder.")
    else:
        # If not in the past, append the message to the reminders
        REMINDERS[rem_time].append(message)
        print(f"Reminder set: '{message}' at {rem_time}")


if __name__ == "__main__":
    print(extract_reminder("Remind me to leave for Movie tonight at 9pm"))