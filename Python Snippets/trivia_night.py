import tkinter as tk
import speech_recognition as sr
import pyttsx3
import requests
import random

class TriviaNightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Night")

        self.categories = self.fetch_categories()
        self.difficulty_levels = ["easy", "medium", "hard"]
        self.selected_category = None
        self.selected_difficulty = None
        self.trivia_questions = []
        self.current_question_index = 0
        self.engine = pyttsx3.init()

        self.label = tk.Label(root, text="Welcome to Trivia Night! Choose your category and difficulty.", wraplength=300)
        self.label.pack(pady=20)

        self.category_label = tk.Label(root, text="Select a category:")
        self.category_label.pack()

        self.category_var = tk.StringVar(value=self.categories[0]["id"])
        for category in self.categories:
            tk.Radiobutton(root, text=category["name"], variable=self.category_var, value=category["id"]).pack(anchor=tk.W)

        self.difficulty_label = tk.Label(root, text="Select difficulty:")
        self.difficulty_label.pack()

        self.difficulty_var = tk.StringVar(value=self.difficulty_levels[0])
        for difficulty in self.difficulty_levels:
            tk.Radiobutton(root, text=difficulty.capitalize(), variable=self.difficulty_var, value=difficulty).pack(anchor=tk.W)

        self.start_button = tk.Button(root, text="Start Trivia", command=self.start_trivia)
        self.start_button.pack(pady=10)

    def fetch_categories(self):
        try:
            response = requests.get("https://opentdb.com/api_category.php")
            return response.json()["trivia_categories"]
        except Exception as e:
            self.label.config(text="Failed to fetch categories.")
            print(e)
            return []

    def start_trivia(self):
        self.selected_category = self.category_var.get()
        self.selected_difficulty = self.difficulty_var.get()
        self.trivia_questions = self.fetch_questions(self.selected_category, self.selected_difficulty)

        if self.trivia_questions:
            random.shuffle(self.trivia_questions)
            self.current_question_index = 0
            self.show_question()
        else:
            self.label.config(text="No questions found for this category and difficulty.")

    def fetch_questions(self, category_id, difficulty):
        try:
            response = requests.get(f"https://opentdb.com/api.php?amount=10&category={category_id}&difficulty={difficulty}&type=multiple")
            data = response.json()
            questions = []
            for item in data["results"]:
                questions.append({
                    "question": item["question"],
                    "correct_answer": item["correct_answer"],
                    "incorrect_answers": item["incorrect_answers"]
                })
            return questions
        except Exception as e:
            self.label.config(text="Failed to fetch questions.")
            print(e)
            return []

    def show_question(self):
        if self.current_question_index < len(self.trivia_questions):
            question_data = self.trivia_questions[self.current_question_index]
            question = question_data["question"]
            self.label.config(text=question)
            self.ask_question(question)
        else:
            self.end_game()

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
                self.check_trivia_answer(answer)
            except sr.UnknownValueError:
                self.label.config(text="Sorry, I did not understand that.")
            except sr.RequestError:
                self.label.config(text="Could not request results from Google Speech Recognition service.")

    def check_trivia_answer(self, user_answer):
        correct_answer = self.trivia_questions[self.current_question_index]["correct_answer"].lower()
        if user_answer == correct_answer:
            self.label.config(text="Correct!")
        else:
            self.label.config(text=f"Incorrect! The correct answer was: {correct_answer}")

        self.current_question_index += 1
        self.show_question()

    def end_game(self):
        self.label.config(text="Thanks for playing Trivia Night! Goodbye!")
        self.engine.say("Thanks for playing Trivia Night! Goodbye!")
        self.engine.runAndWait()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaNightApp(root)
    root.mainloop()
