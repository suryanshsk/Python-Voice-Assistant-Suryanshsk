import tkinter as tk
import random
import speech_recognition as sr
import pyttsx3

class AkinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator Game!")
        self.questions = [
            "Is your character real?",
            "Is your character an animal?",
            "Is your character fictional?",
            "Is your character from a movie?",
            "Is your character a superhero?",
            "Does your character have superpowers?",
            "Is your character a musician?"
        ]
        self.answers = []
        self.current_question = 0

        self.engine = pyttsx3.init()

        self.label = tk.Label(root, text="Welcome to Akinator! Think of a character and answer the questions.", wraplength=300)
        self.label.pack(pady=20)

        self.question_label = tk.Label(root, text="", wraplength=300)
        self.question_label.pack(pady=10)

        self.answer_button_frame = tk.Frame(root)
        self.answer_button_frame.pack(pady=10)

        self.yes_button = tk.Button(self.answer_button_frame, text="Yes", command=self.answer_yes)
        self.yes_button.grid(row=0, column=0, padx=5)

        self.no_button = tk.Button(self.answer_button_frame, text="No", command=self.answer_no)
        self.no_button.grid(row=0, column=1, padx=5)

        self.voice_button = tk.Button(root, text="Speak Your Answer", command=self.get_voice_input)
        self.voice_button.pack(pady=10)

        self.next_question()

    def next_question(self):
        if self.current_question < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question])
            self.ask_question(self.questions[self.current_question])
        else:
            self.final_guess()

    def ask_question(self, question):
        self.engine.say(question)
        self.engine.runAndWait()

    def get_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.config(text="Listening...")
            self.root.update()  # Update the UI
            audio = recognizer.listen(source)
            try:
                answer = recognizer.recognize_google(audio).lower()
                self.label.config(text=f"You said: {answer}")
                print(f"You said: {answer}")
                if answer in ['yes', 'y']:
                    self.answers.append(True)
                    self.current_question += 1
                elif answer in ['no', 'n']:
                    self.answers.append(False)
                    self.current_question += 1
                else:
                    self.label.config(text="Please answer with yes or no.")
                    return
                self.next_question()
            except sr.UnknownValueError:
                self.label.config(text="Sorry, I did not understand that.")
            except sr.RequestError:
                self.label.config(text="Could not request results from Google Speech Recognition service.")

    def answer_yes(self):
        self.answers.append(True)
        self.current_question += 1
        self.next_question()

    def answer_no(self):
        self.answers.append(False)
        self.current_question += 1
        self.next_question()

    def final_guess(self):
        guessed_character = "a character"  # Placeholder for guessing logic
        self.engine.say(f"Is your character {guessed_character}?")
        self.engine.runAndWait()
        self.label.config(text=f"Is your character {guessed_character}?")

        # You can implement a method to accept a final voice answer or button input for yes/no

if __name__ == "__main__":
    root = tk.Tk()
    app = AkinatorApp(root)
    root.mainloop()
