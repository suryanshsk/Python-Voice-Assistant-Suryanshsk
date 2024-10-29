import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def view_upcoming_events(service, max_results=5):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=max_results, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print("No upcoming events found.")
        return
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start}: {event['summary']}")

def create_event(service, summary, description, start_time, end_time):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print("Event created:", event.get('htmlLink'))

def set_reminder(service, reminder_summary, reminder_time):
    event = {
        'summary': reminder_summary,
        'start': {
            'dateTime': reminder_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': reminder_time,
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
                {'method': 'email', 'minutes': 10}
            ],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print("Reminder set:", event.get('htmlLink'))

def main():
    service = authenticate_google_calendar()

    print("Choose an option:")
    print("1. View upcoming events")
    print("2. Create a new event")
    print("3. Set a reminder")

    choice = input("Enter your choice: ")

    if choice == '1':
        view_upcoming_events(service)
    elif choice == '2':
        summary = input("Event summary: ")
        description = input("Event description: ")
        start_time = input("Start time (YYYY-MM-DDTHH:MM:SS): ")
        end_time = input("End time (YYYY-MM-DDTHH:MM:SS): ")
        create_event(service, summary, description, start_time, end_time)
    elif choice == '3':
        reminder_summary = input("Reminder summary: ")
        reminder_time = input("Reminder time (YYYY-MM-DDTHH:MM:SS): ")
        set_reminder(service, reminder_summary, reminder_time)
    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()
