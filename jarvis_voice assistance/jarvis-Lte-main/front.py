import tkinter as tk
from tkinter import scrolledtext
import threading
import jarvis_adv 
import speech_recognition as sr
import pyttsx3

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI Assistant")

        self.output_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.output_text.pack(padx=10, pady=10)

        self.listen_button = tk.Button(root, text="Listen", command=self.listen_command)
        self.listen_button.pack()

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        self.hologram_label = tk.Label(root, text="Hologram here", font=("Arial", 24))
        self.hologram_label.pack()
        self.hologram_moving = False

    def listen_command(self):
        self.output_text.insert(tk.END, "Listening...\n")
        threading.Thread(target=self.process_audio).start()

    def process_audio(self):
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
                user_input = self.recognizer.recognize_google(audio)
                self.output_text.insert(tk.END, f"You (Voice): {user_input}\n")
                response = self.process_command(user_input)
                self.output_text.insert(tk.END, f"Jarvis: {response}\n\n")
                self.speak(response)
                self.animate_hologram()  # Trigger hologram animation
        except sr.UnknownValueError:
            self.output_text.insert(tk.END, "Could not understand the audio.\n")
            self.speak("Could not understand the audio.")
        except sr.RequestError as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
            self.speak("There was an error processing the audio.")

    def process_command(self, command):
        # Call your Jarvis script functions here based on the command
        # For example:
        if 'hello' in command.lower():
            return "Hello! How can I assist you?"
        elif 'play music' in command.lower():
            threading.Thread(target=jarvis_adv.play_music, args=('C:\\path\\to\\music.mp3',)).start()
            return "Playing music..."

        # Add more commands and responses as needed

        else:
            return "Command not recognized."

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def animate_hologram(self):
        if not self.hologram_moving:
            self.hologram_moving = True
            self.move_hologram_left(10)

    def move_hologram_left(self, distance):
        if distance > 0:
            self.root.after(100, self.move_hologram_left, distance - 1)
        else:
            self.hologram_label.place(x=150, y=150)  # Reset the hologram position
            self.hologram_moving = False

            # You can add more complex animations or use libraries like Pygame for smoother animations

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()
