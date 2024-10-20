import os
import google.generativeai as genai
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import pickle
import pyttsx3 as p
import re
from speak import speak



# Set up Google API credentials
os.environ['GOOGLE_API_KEY'] = "your_own_Gemini_api_key"  
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') 
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

# Define the scopes required for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'  # Path to your OAuth 2.0 credentials file
TOKEN_FILE = 'token.pickle'  # File to store the OAuth 2.0 token

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def create_google_meet_event(meeting_name, description, start_time_formatted, end_time_formatted, invitation_emails):
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': meeting_name,
        'description': description,
        'start': {
            'dateTime': start_time_formatted,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time_formatted,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in invitation_emails],
        'conferenceData': {
            'createRequest': {
                'requestId': 'sample123',
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            },
        },
    }

    try:
        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
        print(f'Event created: {event.get("htmlLink")}')
        return event['id']
    except HttpError as error:
        print(f'An error occurred: {error}')
        print(f'Response content: {error.content}')


    
def process_user_input(user_input):
    # Generate response using Gemini
    response = model.generate_content(f"Extract the following information from the given user input: Meeting Name: The title or name of the meeting. Description: A brief description or purpose of the meeting.Start Time: The start time of the meeting.End Time: The end time of the meeting. and convert the start time and end time to this format  start time'2024-08-12T01:00:00+05:30' end time= '2024-08-12T02:00:00+05:30' Invitation Emails: Email addresses of the individuals who should receive the invitation from {user_input}")
    text = response.text
    
    print(response.text)
    
    # Extract details using regex (simplified for demonstration)
    meeting_name_match = re.search(r'Meeting Name:\s*(.*)', text)
    meeting_name = meeting_name_match.group(1).strip() if meeting_name_match else "No meeting name provided"

    # Extracting Description
    description_match = re.search(r'Description:\s*(.*)', text)
    description = description_match.group(1).strip() if description_match else "No description provided"

    # Extracting Start Time
    start_time_formatted = '2024-08-12T01:00:00+05:30'
    end_time_formatted= '2024-08-12T02:00:00+05:30'

    # Extracting Invitation Emails
    emails_matches = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    invitation_emails = [email.strip() for email in emails_matches]

    




    return meeting_name,description,start_time_formatted,end_time_formatted,invitation_emails

if __name__ == "__main__":
    user_input = "Create a Google Meet and schedule a meeting for hackathon at 11:30 PM to 12:00 AM and send the invitation to ravikrishnajayaprakash.aiml2023@citchennai.net and sample@gmail.com"
    meeting_name,description,start_time_formatted,end_time_formatted,invitation_emails = process_user_input(user_input)
    
    # Create the event
    event_id = create_google_meet_event(meeting_name,description,start_time_formatted,end_time_formatted,invitation_emails)
    
    # Speak confirmation
    speak(f'Event created successfully. You can join the meeting using the link: {event_id}')

*


 