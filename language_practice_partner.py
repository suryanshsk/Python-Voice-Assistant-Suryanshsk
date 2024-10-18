import random
import requests
import speech_recognition as sr
from gtts import gTTS
import os
import time

class LanguagePracticePartner:
    def __init__(self):
        self.vocab_quizzes = {
            'beginner': ['cat', 'dog', 'apple'],
            'intermediate': ['university', 'beautiful', 'important'],
            'advanced': ['comprehend', 'perspective', 'analyze']
        }
        self.daily_challenges = [
            "Translate 'Good morning' to Spanish.",
            "Use the word 'exciting' in a sentence.",
            "Write a short paragraph about your day in the target language."
        ]
        self.progress = {
            'conversations': 0,
            'quizzes': 0,
            'pronunciation': 0,
            'challenges': 0
        }
        self.translation_api_url = "https://api.mymemory.translated.net/get"

    def practice_conversation(self):
        print("Let's practice a conversation! Type 'exit' to finish.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            if user_input.strip() == '':
                print("Assistant: Please say something.")
            else:
                print(f"Assistant: Great job! You said: '{user_input}'. Keep practicing!")
                self.progress['conversations'] += 1

    def vocabulary_quiz(self):
        level = input("Choose your proficiency level (beginner, intermediate, advanced): ").lower()
        if level in self.vocab_quizzes:
            words = self.vocab_quizzes[level]
            random_word = random.choice(words)
            answer = input(f"What is the translation of '{random_word}'? ")
            correct_answer = self.get_translation(random_word)
            if answer.lower() == correct_answer:
                print("Correct! Well done.")
            else:
                print(f"Incorrect. The correct answer is: {correct_answer}.")
            self.progress['quizzes'] += 1
        else:
            print("Invalid level. Please try again.")

    def get_translation(self, word):
        response = requests.get(self.translation_api_url, params={'q': word, 'langpair': 'en|es'})
        data = response.json()
        return data['responseData']['translatedText']

    def pronunciation_assistance(self):
        print("Please say a word or phrase...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: '{text}'.")
                self.provide_pronunciation_feedback(text)
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError:
                print("Could not request results from the speech recognition service.")
            self.progress['pronunciation'] += 1

    def provide_pronunciation_feedback(self, text):
        # This is a simple implementation; you can enhance this further.
        # Here we could compare against a reference pronunciation.
        print(f"Assistant: Great job saying '{text}'!")

        # Provide spoken feedback using text-to-speech
        tts = gTTS(f"Great job saying {text}!", lang='en')
        tts.save("feedback.mp3")
        os.system("start feedback.mp3")
        time.sleep(2)  # Wait for the audio to finish playing
        os.remove("feedback.mp3")  # Clean up

    def daily_language_challenge(self):
        challenge = random.choice(self.daily_challenges)
        print(f"Today's challenge: {challenge}")
        self.progress['challenges'] += 1

    def display_progress(self):
        print("\nYour Progress:")
        for activity, count in self.progress.items():
            print(f"{activity.capitalize()}: {count} sessions completed.")
        print("\nKeep up the good work!")

    def main_menu(self):
        while True:
            print("\n--- Language Practice Partner ---")
            print("1. Practice Conversations")
            print("2. Vocabulary Quiz")
            print("3. Pronunciation Assistance")
            print("4. Daily Language Challenge")
            print("5. Display Progress")
            print("6. Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                self.practice_conversation()
            elif choice == '2':
                self.vocabulary_quiz()
            elif choice == '3':
                self.pronunciation_assistance()
            elif choice == '4':
                self.daily_language_challenge()
            elif choice == '5':
                self.display_progress()
            elif choice == '6':
                print("Goodbye! Keep practicing.")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    partner = LanguagePracticePartner()
    partner.main_menu()
