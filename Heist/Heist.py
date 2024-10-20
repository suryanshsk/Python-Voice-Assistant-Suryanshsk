import speech_recognition as sr
import pyttsx3
import random

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return listen()
        except sr.RequestError:
            speak("Sorry, there seems to be an issue with the speech service.")
            return None

def choose_heist(heists):
    heist_names = ", ".join(heists.keys())
    speak(f"Choose your heist from the following options: {heist_names}.")
    user_input = listen()
    if user_input in heists:
        return user_input
    else:
        speak("That's not a valid choice. Please choose again.")
        return choose_heist(heists)

def run_heist(story_title, scenarios):
    speak(f"Welcome to {story_title}. Let's begin!")
    for scenario in scenarios:
        speak(scenario['prompt'])
        user_input = listen()
        if user_input in scenario['success_choices']:
            speak(scenario['success_message'])
        else:
            speak(scenario['failure_message'])
            break

heists = {
    "The Art of Deception": [
        {
            'prompt': "You need to gain entry to the exhibition. What do you do?",
            'success_choices': ["steal the invitation", "get the invitation"],
            'success_message': "You successfully lift the invitation.",
            'failure_message': "You get caught and thrown out!"
        },
        {
            'prompt': "Learn the layout of the gallery. What do you do?",
            'success_choices': ["search the pamphlet"],
            'success_message': "You find the pamphlet with valuable info.",
            'failure_message': "You get lost in the gallery!"
        },
        {
            'prompt': "Acquire disguises to blend in. What do you do?",
            'success_choices': ["visit the rental shop"],
            'success_message': "You acquire convincing outfits.",
            'failure_message': "A guard spots you as suspicious!"
        },
        {
            'prompt': "Disable the alarm system. What do you do?",
            'success_choices': ["contact the former employee"],
            'success_message': "You get the security codes.",
            'failure_message': "An unexpected alarm triggers!"
        },
        {
            'prompt': "Escape with the painting. What do you do?",
            'success_choices': ["use the service entrance"],
            'success_message': "You slip out undetected with the painting!",
            'failure_message': "You are caught by the police!"
        }
    ],
    "The Museum Heist": [
        {
            'prompt': "Gather information on the museum’s security. What do you do?",
            'success_choices': ["check the bulletin board"],
            'success_message': "You gather guard shift timings.",
            'failure_message': "You miss critical schedule changes!"
        },
        {
            'prompt': "Enter the museum undetected. What do you do?",
            'success_choices': ["wait for the right moment"],
            'success_message': "You enter without raising alarms.",
            'failure_message': "You trigger an alarm!"
        },
        {
            'prompt': "Create a diversion. What do you do?",
            'success_choices': ["hire the performer"],
            'success_message': "The performer creates chaos.",
            'failure_message': "You attract attention from the guards!"
        },
        {
            'prompt': "Access the display case. What do you do?",
            'success_choices': ["use a lock-picking tool"],
            'success_message': "You unlock the case and retrieve the artifact.",
            'failure_message': "You trigger the alarm!"
        },
        {
            'prompt': "Get away safely. What do you do?",
            'success_choices': ["head to the alley"],
            'success_message': "You escape in the vehicle.",
            'failure_message': "You run into a police checkpoint!"
        }
    ],
    "The Casino Caper": [
        {
            'prompt': "Create a plan for the heist. What do you do?",
            'success_choices': ["research the layout"],
            'success_message': "You gain a detailed understanding.",
            'failure_message': "You get confused!"
        },
        {
            'prompt': "Gain access to the poker tournament. What do you do?",
            'success_choices': ["approach the gambler"],
            'success_message': "You acquire the VIP tickets.",
            'failure_message': "Security catches you!"
        },
        {
            'prompt': "Cause a distraction. What do you do?",
            'success_choices': ["trigger the fire alarm"],
            'success_message': "The casino evacuates.",
            'failure_message': "It raises suspicion!"
        },
        {
            'prompt': "Access the chip and cash storage. What do you do?",
            'success_choices': ["steal a keycard"],
            'success_message': "You access the storage undetected.",
            'failure_message': "You get caught!"
        },
        {
            'prompt': "Escape the casino. What do you do?",
            'success_choices': ["make your way to the garage"],
            'success_message': "You drive away with the loot!",
            'failure_message': "You are intercepted by security!"
        }
    ],
    "The Bank Job": [
        {
            'prompt': "Monitor the bank's security systems. What do you do?",
            'success_choices': ["watch from the café"],
            'success_message': "You note the guard changes.",
            'failure_message': "You get caught!"
        },
        {
            'prompt': "Recruit an inside man. What do you do?",
            'success_choices': ["contact the employee"],
            'success_message': "You get valuable intel.",
            'failure_message': "You miss out on crucial information!"
        },
        {
            'prompt': "Acquire the necessary tools for the heist. What do you do?",
            'success_choices': ["visit the store"],
            'success_message': "You gather tools without attention.",
            'failure_message': "They fail during the heist!"
        },
        {
            'prompt': "Access the bank vault. What do you do?",
            'success_choices': ["use the inside man’s access"],
            'success_message': "You enter the vault.",
            'failure_message': "You trigger an alarm!"
        },
        {
            'prompt': "Flee the scene. What do you do?",
            'success_choices': ["follow the escape route"],
            'success_message': "You evade capture and drive away.",
            'failure_message': "You reach a police roadblock!"
        }
    ],
    "The Tech Theft": [
        {
            'prompt': "Gather intel about the prototype. What do you do?",
            'success_choices': ["look up the documents"],
            'success_message': "You gather key information.",
            'failure_message': "You miss crucial details!"
        },
        {
            'prompt': "Get into the building. What do you do?",
            'success_choices': ["wait for lunch hour"],
            'success_message': "You slip in unnoticed.",
            'failure_message': "You get caught!"
        },
        {
            'prompt': "Blend in with employees. What do you do?",
            'success_choices': ["purchase uniforms"],
            'success_message': "You fit right in.",
            'failure_message': "You attract attention!"
        },
        {
            'prompt': "Access the prototype room. What do you do?",
            'success_choices': ["steal a keycard"],
            'success_message': "You enter the room.",
            'failure_message': "You trigger the alarm!"
        },
        {
            'prompt': "Escape with the prototype. What do you do?",
            'success_choices': ["head to the alley"],
            'success_message': "You escape with the prototype!",
            'failure_message': "You are intercepted by security!"
        }
    ]
}

selected_heist = choose_heist(heists)
run_heist(selected_heist, heists[selected_heist])