import speech_recognition as sr
import pyttsx3
import time

class QuestionNode:
    def __init__(self, question):
        self.question = question
        self.yes = None
        self.no = None

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            answer = recognizer.recognize_google(audio)
            print(f"You said: {answer}")
            return answer.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you please repeat?")
            return listen()
        except sr.RequestError:
            speak("There was a problem with the service. Please try again later.")
            return None

def ask_question(node):
    if node.yes is None and node.no is None:
        return node.question

    speak(node.question)
    answer = listen()
    
    if answer == 'yes':
        return ask_question(node.yes)
    elif answer == 'no':
        return ask_question(node.no)
    else:
        speak("I didn't understand that. Please say 'yes' or 'no'.")
        return ask_question(node)

def add_new_thing(node, question, new_thing):
    new_node = QuestionNode(question)
    new_node.yes = QuestionNode(new_thing)
    new_node.no = node
    return new_node

def main():
    root = QuestionNode("Is it an animal?")
    
    # Expanding the decision tree with more questions and animals
    root.yes = QuestionNode("Is it a mammal?")
    root.yes.yes = QuestionNode("Does it have fur?")
    root.yes.yes.yes = QuestionNode("Is it a dog?")
    root.yes.yes.no = QuestionNode("Is it a cat?")
    root.yes.no = QuestionNode("Is it a reptile?")
    root.yes.no.yes = QuestionNode("Is it a snake?")
    root.yes.no.no = QuestionNode("Is it a bird?")
    root.yes.no.no.yes = QuestionNode("Is it a parrot?")
    root.yes.no.no.no = QuestionNode("I can't guess that one.")
    
    root.no = QuestionNode("Is it a vegetable?")
    root.no.yes = QuestionNode("Is it leafy?")
    root.no.yes.yes = QuestionNode("Is it lettuce?")
    root.no.yes.no = QuestionNode("Is it a root vegetable?")
    root.no.yes.no.yes = QuestionNode("Is it a carrot?")
    root.no.yes.no.no = QuestionNode("I can't guess that one.")
    
    root.no.no = QuestionNode("I can't guess that one.")

    speak("Hi there! Let's play a game of 20 Questions.")
    time.sleep(1)

    while True:
        speak("Think of something, and I'll try to guess what it is.")
        time.sleep(1)
        guess = ask_question(root)
        speak(f"I guess it's: {guess}")

        if guess == "I can't guess that one.":
            speak("Oh no! What were you thinking of?")
            new_thing = input("What were you thinking of? ")
            question = input(f"What question would help me know the difference between a {new_thing} and {guess}? ")
            root = add_new_thing(root, question, new_thing)
        
        speak("Would you like to play again? Please say 'yes' or 'no'.")
        play_again = listen()
        if play_again != 'yes':
            break

    speak("Thanks for playing! Have a great day!")

if __name__ == "__main__":
    main()
