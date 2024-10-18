##Requirements
#pip install speechrecognition pyttsx3 twilio tweepy


import smtplib
import speech_recognition as sr
import pyttsx3
from twilio.rest import Client
import tweepy

# Text to Speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Email Functionality
def send_email(to_email, subject, message):
    from_email = "your_email@example.com"
    password = "your_email_password"  # Use app password if enabled

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(from_email, to_email, email_message)

# SMS Functionality
def send_sms(to_phone, message):
    account_sid = 'your_twilio_account_sid'
    auth_token = 'your_twilio_auth_token'
    client = Client(account_sid, auth_token)

    client.messages.create(
        to=to_phone,
        from_='your_twilio_phone_number',
        body=message
    )

# WhatsApp Functionality
def send_whatsapp(to_phone, message):
    account_sid = 'your_twilio_account_sid'
    auth_token = 'your_twilio_auth_token'
    client = Client(account_sid, auth_token)

    client.messages.create(
        to=f'whatsapp:{to_phone}',
        from_='whatsapp:your_twilio_whatsapp_number',
        body=message
    )

# Twitter Posting Functionality
def post_tweet(message):
    consumer_key = 'your_twitter_consumer_key'
    consumer_secret = 'your_twitter_consumer_secret'
    access_token = 'your_twitter_access_token'
    access_token_secret = 'your_twitter_access_token_secret'

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    api.update_status(message)

# Voice Command Functionality
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""

# Main Function
def main():
    speak("Welcome to your voice-controlled assistant.")
    while True:
        command = listen_command()

        if "send email" in command:
            speak("Who is the recipient?")
            recipient = listen_command()
            speak("What is the subject?")
            subject = listen_command()
            speak("What is the message?")
            message = listen_command()
            send_email(recipient, subject, message)
            speak("Email sent.")

        elif "send sms" in command:
            speak("What is the phone number?")
            phone_number = listen_command()
            speak("What is your message?")
            message = listen_command()
            send_sms(phone_number, message)
            speak("SMS sent.")

        elif "send whatsapp" in command:
            speak("What is the phone number?")
            phone_number = listen_command()
            speak("What is your message?")
            message = listen_command()
            send_whatsapp(phone_number, message)
            speak("WhatsApp message sent.")

        elif "post tweet" in command:
            speak("What would you like to tweet?")
            message = listen_command()
            post_tweet(message)
            speak("Tweet posted.")

        elif "exit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
