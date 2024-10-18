import datetime
import speech_recognition as sr
import pyttsx3

class TimeCapsule:
    def __init__(self):
        self.capsules = []
        self.password = "securepassword"  # Set your password here

    def record_message(self, message, release_date):
        """Record a new time capsule message."""
        if release_date < datetime.datetime.now().date():
            return "🚫 Oops! The release date must be in the future. Can you try again?"
        
        capsule = {
            'message': message,
            'release_date': release_date,
            'revealed': False
        }
        self.capsules.append(capsule)
        return f"🌟 Your message has been safely stored! It will be revealed on {release_date.strftime('%Y-%m-%d')}."

    def check_capsules(self):
        """Check and reveal any messages that should be visible now."""
        today = datetime.datetime.now().date()
        revealed_messages = []
        remaining_capsules = []

        for capsule in self.capsules:
            if not capsule['revealed'] and today >= capsule['release_date']:
                revealed_messages.append(capsule['message'])
                capsule['revealed'] = True
            else:
                remaining_capsules.append(capsule)

        self.capsules = remaining_capsules  # Clean up revealed capsules
        return revealed_messages if revealed_messages else ["⏳ No messages are ready to be revealed just yet!"]

    def view_capsules(self):
        """View the status of stored capsules."""
        if not self.capsules:
            return ["📦 You haven't stored any messages in your time capsule yet."]
        
        capsule_list = []
        for i, capsule in enumerate(self.capsules, 1):
            status = "✅ Revealed" if capsule['revealed'] else f"🔒 Hidden until {capsule['release_date'].strftime('%Y-%m-%d')}"
            capsule_list.append(f"{i}. Status: {status}")

        return capsule_list

    def edit_capsule(self, index, new_message):
        """Edit an existing capsule message with password verification."""
        if 0 <= index < len(self.capsules):
            entered_password = input("🔒 Please enter your password to proceed: ")
            if entered_password == self.password:
                old_message = self.capsules[index]['message']
                self.capsules[index]['message'] = new_message
                return f"✏️ Your message has been updated from '{old_message}' to '{new_message}'."
            else:
                return "🚫 Action cancelled. Incorrect password."
        return "🚫 Error: Invalid capsule index! Please try again."

    def delete_capsule(self, index):
        """Delete a capsule."""
        if 0 <= index < len(self.capsules):
            removed_message = self.capsules.pop(index)['message']
            return f"🗑️ The message '{removed_message}' has been successfully deleted from your time capsule."
        return "🚫 Error: Invalid capsule index! Can't delete that."

    def search_capsules(self, keyword):
        """Search for messages containing the keyword."""
        found_messages = [capsule for capsule in self.capsules if keyword.lower() in capsule['message'].lower()]
        if found_messages:
            return [f"Message: '{capsule['message']}' | Release Date: {capsule['release_date'].strftime('%Y-%m-%d')}" for capsule in found_messages]
        return ["🔍 No messages found containing that keyword."]

    def sort_capsules(self, by='date'):
        """Sort capsules by release date or status."""
        if by == 'date':
            self.capsules.sort(key=lambda x: x['release_date'])
            return "🗂️ Capsules sorted by release date."
        elif by == 'status':
            self.capsules.sort(key=lambda x: x['revealed'])
            return "🗂️ Capsules sorted by status."
        return "🚫 Invalid sort option!"

# Voice Interaction Setup
def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("👂 Sorry, I could not understand you.")
            return ""
        except sr.RequestError:
            print("⚠️ Could not request results from Google Speech Recognition service.")
            return ""

# Example integration into a main assistant app
def main_assistant():
    time_capsule = TimeCapsule()
    
    speak("Hello! Welcome to your Time Capsule Assistant! Ready to store your precious memories?")
    
    while True:
        speak("What would you like to do? You can say record, check, view, edit, delete, search, sort, help, or exit.")
        command = listen()

        if "record" in command:
            speak("Please tell me your message.")
            message = listen()
            speak("When would you like this message to be revealed? Please say the date in YYYY-MM-DD format.")
            release_date_input = listen()
            try:
                release_date = datetime.datetime.strptime(release_date_input, '%Y-%m-%d').date()
                response = time_capsule.record_message(message, release_date)
                speak(response)
            except ValueError:
                speak("🚫 Invalid date format. Please try again.")

        elif "check" in command:
            revealed_messages = time_capsule.check_capsules()
            for msg in revealed_messages:
                speak(f"Revealed message: {msg}")

        elif "view" in command:
            capsules = time_capsule.view_capsules()
            for item in capsules:
                speak(item)

        elif "edit" in command:
            speak("Which message would you like to edit? Please provide the index number.")
            index_input = listen()
            try:
                index = int(index_input) - 1
                speak("Please tell me your new message.")
                new_message = listen()
                response = time_capsule.edit_capsule(index, new_message)
                speak(response)
            except (ValueError, IndexError):
                speak("🚫 Invalid input. Please try again.")

        elif "delete" in command:
            speak("Which message would you like to delete? Please provide the index number.")
            index_input = listen()
            try:
                index = int(index_input) - 1
                response = time_capsule.delete_capsule(index)
                speak(response)
            except (ValueError, IndexError):
                speak("🚫 Invalid input. Please try again.")

        elif "search" in command:
            speak("Please say a keyword to search for.")
            keyword = listen()
            results = time_capsule.search_capsules(keyword)
            for result in results:
                speak(result)

        elif "sort" in command:
            speak("Would you like to sort by date or status?")
            sort_by = listen()
            response = time_capsule.sort_capsules(by=sort_by)
            speak(response)

        elif "help" in command:
            speak("Here are the commands you can use: record, check, view, edit, delete, search, sort, or exit.")

        elif "exit" in command:
            speak("Thank you for using the Time Capsule Assistant! Keep cherishing your memories! Goodbye!")
            break

        else:
            speak("Hmm, I didn't quite catch that. Can you please try again?")

if __name__ == "__main__":
    main_assistant()
