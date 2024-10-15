import speech_recognition as sr
import pyttsx3
import random

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Define crime cases with clues, suspects, and character profiles
cases = {
    "Case 1": {
        "scenario": "A valuable painting was stolen from the art gallery.",
        "clues": [
            {"type": "evidence", "text": "The security guard heard a strange noise at 3 AM."},
            {"type": "evidence", "text": "The thief left behind a footprint."},
            {"type": "witness", "text": "A witness saw a man in a red jacket near the gallery."}
        ],
        "suspects": {
            "The Security Guard": {
                "motive": "He wanted to steal the painting and sell it on the black market.",
                "alibi": "He was at his post the whole time."
            },
            "The Known Art Thief": {
                "motive": "He has a history of stealing valuable art.",
                "alibi": "He claims he was in a different city."
            },
            "The Visitor in a Red Jacket": {
                "motive": "He wanted to impress a wealthy friend.",
                "alibi": "He says he left the gallery before the theft."
            }
        },
        "solution": "The Visitor in a Red Jacket."
    },
    "Case 2": {
        "scenario": "A bank was robbed in broad daylight.",
        "clues": [
            {"type": "evidence", "text": "The robber wore a blue mask."},
            {"type": "evidence", "text": "A getaway car was seen speeding away."},
            {"type": "witness", "text": "One of the bank tellers recognized the robber."}
        ],
        "suspects": {
            "The Bank Manager": {
                "motive": "He wanted to pay off debts.",
                "alibi": "He was in his office at the time."
            },
            "The Former Employee": {
                "motive": "He was fired and wanted revenge.",
                "alibi": "He was at a bar nearby."
            },
            "The Street Vendor": {
                "motive": "He needed money for his family.",
                "alibi": "He was serving customers."
            }
        },
        "solution": "The Former Employee."
    },
    "Case 3": {
        "scenario": "A murder took place at a party.",
        "clues": [
            {"type": "evidence", "text": "The victim was last seen arguing with someone."},
            {"type": "evidence", "text": "There were fingerprints on the wine glass."},
            {"type": "witness", "text": "A guest heard a loud crash before the scream."}
        ],
        "suspects": {
            "The Host of the Party": {
                "motive": "He was jealous of the victim's success.",
                "alibi": "He claims he was in the kitchen preparing snacks."
            },
            "The Victim's Friend": {
                "motive": "They had a falling out recently.",
                "alibi": "She was in the bathroom during the incident."
            },
            "A Mysterious Guest": {
                "motive": "He was looking for a rare item the victim had.",
                "alibi": "He says he was outside on a phone call."
            }
        },
        "solution": "The Host of the Party."
    },
    "Case 4": {
        "scenario": "A rare jewel was stolen during a gala.",
        "clues": [
            {"type": "evidence", "text": "A server saw someone slip away with a bag."},
            {"type": "evidence", "text": "There were security cameras, but they were turned off."},
            {"type": "witness", "text": "A guest reported a suspicious person near the exit."}
        ],
        "suspects": {
            "The Server": {
                "motive": "He wanted to sell the jewel to pay off debts.",
                "alibi": "He was busy serving drinks."
            },
            "The Gala Organizer": {
                "motive": "She wanted the insurance money.",
                "alibi": "She was talking to guests."
            },
            "A Guest in a Black Suit": {
                "motive": "He had a secret connection to the jewel's owner.",
                "alibi": "He claims he was on the dance floor."
            }
        },
        "solution": "The Gala Organizer."
    },
    "Case 5": {
        "scenario": "A scientist was poisoned in his lab.",
        "clues": [
            {"type": "evidence", "text": "The lab was locked from the inside."},
            {"type": "evidence", "text": "A vial of poison was found missing."},
            {"type": "witness", "text": "The victim had been arguing with a colleague."}
        ],
        "suspects": {
            "The Colleague": {
                "motive": "He wanted to take credit for the victim's research.",
                "alibi": "He was in a different lab at the time."
            },
            "The Lab Assistant": {
                "motive": "She was unhappy with her job and wanted revenge.",
                "alibi": "She claims she was cleaning equipment."
            },
            "A Rival Scientist": {
                "motive": "He was jealous of the victim's success.",
                "alibi": "He says he was at a conference."
            }
        },
        "solution": "The Colleague."
    },
    "Case 6": {
        "scenario": "A famous chef was found dead in his kitchen.",
        "clues": [
            {"type": "evidence", "text": "There were traces of poison in his last meal."},
            {"type": "evidence", "text": "A knife was missing from the kitchen."},
            {"type": "witness", "text": "A staff member heard shouting just before the body was found."}
        ],
        "suspects": {
            "The Sous Chef": {
                "motive": "He wanted to take over the restaurant.",
                "alibi": "He was preparing another dish."
            },
            "The Restaurant Owner": {
                "motive": "He was losing money and wanted to cash in on insurance.",
                "alibi": "He was meeting a supplier."
            },
            "A Food Critic": {
                "motive": "He had a personal grudge against the chef.",
                "alibi": "He was outside smoking."
            }
        },
        "solution": "The Sous Chef."
    },
    "Case 7": {
        "scenario": "A politician's campaign office was vandalized.",
        "clues": [
            {"type": "evidence", "text": "The words 'Liar' were spray-painted on the wall."},
            {"type": "evidence", "text": "A broken window was found at the back."},
            {"type": "witness", "text": "A neighbor saw a hooded figure fleeing the scene."}
        ],
        "suspects": {
            "A Rival Politician": {
                "motive": "He wanted to sabotage the campaign.",
                "alibi": "He was attending a fundraiser."
            },
            "An Angry Voter": {
                "motive": "He was upset over a recent policy change.",
                "alibi": "He claims he was at home."
            },
            "A Campaign Intern": {
                "motive": "He disagreed with the politician's approach.",
                "alibi": "He was out running errands."
            }
        },
        "solution": "The Rival Politician."
    },
    "Case 8": {
        "scenario": "A tech company was hacked, and sensitive data was leaked.",
        "clues": [
            {"type": "evidence", "text": "The hack originated from inside the company."},
            {"type": "evidence", "text": "An employee's computer was accessed without authorization."},
            {"type": "witness", "text": "A janitor saw someone in the office late at night."}
        ],
        "suspects": {
            "The IT Manager": {
                "motive": "He wanted to sell the data to a competitor.",
                "alibi": "He was at a meeting."
            },
            "A Junior Developer": {
                "motive": "She was frustrated with her job and wanted revenge.",
                "alibi": "She claims she was working late on a project."
            },
            "The CEO": {
                "motive": "He wanted to cover up a financial scandal.",
                "alibi": "He was traveling on business."
            }
        },
        "solution": "The Junior Developer."
    },
    "Case 9": {
        "scenario": "A high-profile journalist was found dead in her apartment.",
        "clues": [
            {"type": "evidence", "text": "There were signs of a struggle in the living room."},
            {"type": "evidence", "text": "A threatening note was found on her desk."},
            {"type": "witness", "text": "A neighbor heard loud noises coming from her apartment."}
        ],
        "suspects": {
            "An Ex-Partner": {
                "motive": "He was jealous of her success.",
                "alibi": "He was at a friend's house."
            },
            "A Colleague": {
                "motive": "They were in competition for a major story.",
                "alibi": "He was at a press conference."
            },
            "A Stalker": {
                "motive": "He was obsessed with her work.",
                "alibi": "He claims he was at a bar."
            }
        },
        "solution": "The Ex-Partner."
    },
    "Case 10": {
        "scenario": "A beloved teacher was found poisoned in the staff room.",
        "clues": [
            {"type": "evidence", "text": "A bottle of poison was found in the teacher's desk."},
            {"type": "evidence", "text": "There were no signs of forced entry."},
            {"type": "witness", "text": "A student saw a suspicious figure leaving the staff room."}
        ],
        "suspects": {
            "A Fellow Teacher": {
                "motive": "She was envious of the teacher's popularity.",
                "alibi": "She was in a meeting during lunch."
            },
            "A Parent": {
                "motive": "He was unhappy with a recent grade his child received.",
                "alibi": "He claims he was at work."
            },
            "A Student": {
                "motive": "He had a grudge due to a disciplinary action.",
                "alibi": "He says he was in the library."
            }
        },
        "solution": "A Fellow Teacher."
    },
    "Case 11": {
        "scenario": "A famous singer's jewelry collection was stolen.",
        "clues": [
            {"type": "evidence", "text": "The alarm system was disabled before the theft."},
            {"type": "evidence", "text": "A window was found ajar."},
            {"type": "witness", "text": "A neighbor saw a suspicious car parked outside."}
        ],
        "suspects": {
            "The Assistant": {
                "motive": "She wanted to start her own career.",
                "alibi": "She claims she was at a rehearsal."
            },
            "An Ex-Boyfriend": {
                "motive": "He was bitter after their breakup.",
                "alibi": "He was at a friend's house."
            },
            "A Fan": {
                "motive": "He was obsessed with the singer.",
                "alibi": "He says he was at a concert."
            }
        },
        "solution": "The Assistant."
    },
    "Case 12": {
        "scenario": "A scientist's lab notebook was stolen just before a big presentation.",
        "clues": [
            {"type": "evidence", "text": "There was a struggle in the lab."},
            {"type": "evidence", "text": "A note with a threat was found in the drawer."},
            {"type": "witness", "text": "A student saw someone leaving with a bag."}
        ],
        "suspects": {
            "A Rival Researcher": {
                "motive": "He wanted to sabotage the presentation.",
                "alibi": "He claims he was at a conference."
            },
            "A Lab Intern": {
                "motive": "She wanted to impress a professor.",
                "alibi": "She was working on her project."
            },
            "The Professor": {
                "motive": "He wanted to keep his research undisputed.",
                "alibi": "He was grading papers."
            }
        },
        "solution": "A Rival Researcher."
    },
    "Case 13": {
        "scenario": "A popular game developer was found dead in his office.",
        "clues": [
            {"type": "evidence", "text": "The office was locked from the inside."},
            {"type": "evidence", "text": "A gaming trophy was broken."},
            {"type": "witness", "text": "A coworker heard loud noises before the body was found."}
        ],
        "suspects": {
            "A Co-Developer": {
                "motive": "He wanted to take credit for the project.",
                "alibi": "He claims he was at lunch."
            },
            "An Angry Fan": {
                "motive": "He was upset about a game delay.",
                "alibi": "He was at home."
            },
            "The Assistant": {
                "motive": "She was tired of being overlooked.",
                "alibi": "She was organizing files."
            }
        },
        "solution": "A Co-Developer."
    },
    "Case 14": {
        "scenario": "A prominent lawyer was found poisoned at a dinner party.",
        "clues": [
            {"type": "evidence", "text": "The poison was in his wine glass."},
            {"type": "evidence", "text": "A broken glass was found on the floor."},
            {"type": "witness", "text": "A guest heard an argument shortly before the victim collapsed."}
        ],
        "suspects": {
            "A Rival Lawyer": {
                "motive": "He wanted to eliminate competition.",
                "alibi": "He claims he was in the restroom."
            },
            "A Client": {
                "motive": "He was unhappy with the lawyer's representation.",
                "alibi": "He says he was outside."
            },
            "A Family Member": {
                "motive": "They had a longstanding feud.",
                "alibi": "She was talking to other guests."
            }
        },
        "solution": "A Rival Lawyer."
    },
    "Case 15": {
        "scenario": "A famous author was found dead in her study.",
        "clues": [
            {"type": "evidence", "text": "A manuscript was missing."},
            {"type": "evidence", "text": "There were signs of forced entry."},
            {"type": "witness", "text": "A neighbor saw a stranger leaving the house."}
        ],
        "suspects": {
            "A Literary Agent": {
                "motive": "He wanted to control the author's work.",
                "alibi": "He was at a meeting."
            },
            "A Jealous Writer": {
                "motive": "He was envious of her success.",
                "alibi": "He claims he was at a bar."
            },
            "A Family Member": {
                "motive": "They wanted the inheritance.",
                "alibi": "He was out running errands."
            }
        },
        "solution": "A Jealous Writer."
    },
    "Case 16": {
        "scenario": "A renowned architect was found dead in his office.",
        "clues": [
            {"type": "evidence", "text": "A blueprint for a new project was missing."},
            {"type": "evidence", "text": "There was a strange odor in the air."},
            {"type": "witness", "text": "A security guard saw someone leave the building late at night."}
        ],
        "suspects": {
            "A Business Partner": {
                "motive": "He wanted full control of the firm.",
                "alibi": "He claims he was out of town."
            },
            "An Assistant": {
                "motive": "She was tired of being underappreciated.",
                "alibi": "She was working overtime."
            },
            "A Rival Architect": {
                "motive": "He wanted to ruin the architect's reputation.",
                "alibi": "He was attending a seminar."
            }
        },
        "solution": "A Business Partner."
    },
    "Case 17": {
        "scenario": "A social media influencer was blackmailed.",
        "clues": [
            {"type": "evidence", "text": "Threatening messages were found on her phone."},
            {"type": "evidence", "text": "A security video showed someone entering her home."},
            {"type": "witness", "text": "A neighbor heard a loud argument."}
        ],
        "suspects": {
            "A Former Friend": {
                "motive": "She was jealous of the influencer's success.",
                "alibi": "She claims she was at a party."
            },
            "A Stalker": {
                "motive": "He was obsessed with her online persona.",
                "alibi": "He says he was at home."
            },
            "An Ex-Manager": {
                "motive": "He wanted revenge after being fired.",
                "alibi": "He was traveling."
            }
        },
        "solution": "A Former Friend."
    },
    "Case 18": {
        "scenario": "A successful entrepreneur was found dead in his mansion.",
        "clues": [
            {"type": "evidence", "text": "A broken vase was found near the body."},
            {"type": "evidence", "text": "His bank accounts were accessed just before his death."},
            {"type": "witness", "text": "A gardener saw someone leave the mansion."}
        ],
        "suspects": {
            "A Business Rival": {
                "motive": "He wanted to eliminate competition.",
                "alibi": "He was at a conference."
            },
            "A Family Member": {
                "motive": "She wanted to inherit the fortune.",
                "alibi": "She was at a charity event."
            },
            "A Housekeeper": {
                "motive": "She was unhappy with her pay.",
                "alibi": "She was cleaning the garage."
            }
        },
        "solution": "A Business Rival."
    },
    "Case 19": {
        "scenario": "A famous actor was found dead on set.",
        "clues": [
            {"type": "evidence", "text": "The prop gun was found loaded."},
            {"type": "evidence", "text": "There was a note threatening the actor."},
            {"type": "witness", "text": "A crew member heard a loud bang."}
        ],
        "suspects": {
            "The Director": {
                "motive": "He wanted to boost the drama of the film.",
                "alibi": "He was reviewing footage."
            },
            "A Co-Star": {
                "motive": "She was envious of the actor's fame.",
                "alibi": "She claims she was in her trailer."
            },
            "A Stunt Double": {
                "motive": "He wanted the lead role.",
                "alibi": "He says he was in the gym."
            }
        },
        "solution": "The Co-Star."
    },
    "Case 20": {
        "scenario": "A startup's confidential project was leaked.",
        "clues": [
            {"type": "evidence", "text": "An employee's computer was accessed without permission."},
            {"type": "evidence", "text": "A file with sensitive information was missing."},
            {"type": "witness", "text": "A delivery person saw someone acting suspiciously."}
        ],
        "suspects": {
            "The Lead Developer": {
                "motive": "He wanted to sell the information to a rival company.",
                "alibi": "He was at a team meeting."
            },
            "An Intern": {
                "motive": "She was hoping to impress a recruiter.",
                "alibi": "She claims she was fetching coffee."
            },
            "The CEO": {
                "motive": "He wanted to cover up a previous mistake.",
                "alibi": "He was in a different office."
            }
        },
        "solution": "The Intern."
    },
    "Case 21": {
        "scenario": "A championship trophy was stolen before the game.",
        "clues": [
            {"type": "evidence", "text": "The trophy case was broken into."},
            {"type": "evidence", "text": "A security guard saw a player near the case."},
            {"type": "witness", "text": "A fan reported seeing someone acting suspiciously."}
        ],
        "suspects": {
            "A Rival Team Player": {
                "motive": "He wanted to sabotage the competition.",
                "alibi": "He claims he was practicing."
            },
            "The Team Coach": {
                "motive": "He wanted to distract the team.",
                "alibi": "He was in a meeting."
            },
            "A Die-Hard Fan": {
                "motive": "He wanted to keep the trophy safe.",
                "alibi": "He says he was at home."
            }
        },
        "solution": "A Rival Team Player."
    },
    "Case 22": {
        "scenario": "A museum exhibit was vandalized overnight.",
        "clues": [
            {"type": "evidence", "text": "Security footage was tampered with."},
            {"type": "evidence", "text": "There were paint stains found on the floor."},
            {"type": "witness", "text": "A night guard heard noises."}
        ],
        "suspects": {
            "A Rival Artist": {
                "motive": "He was jealous of the exhibit's success.",
                "alibi": "He claims he was at a gallery opening."
            },
            "A Museum Curator": {
                "motive": "He wanted to change the exhibit.",
                "alibi": "He was at home."
            },
            "A Teenager": {
                "motive": "He wanted to impress his friends.",
                "alibi": "He says he was out skateboarding."
            }
        },
        "solution": "A Rival Artist."
    },
    "Case 23": {
        "scenario": "A car was found abandoned after a hit-and-run.",
        "clues": [
            {"type": "evidence", "text": "The car's license plate was traced to a local dealer."},
            {"type": "evidence", "text": "Paint residue matched a nearby vehicle."},
            {"type": "witness", "text": "A pedestrian saw the accident."}
        ],
        "suspects": {
            "A Local Mechanic": {
                "motive": "He wanted to cover up his own accident.",
                "alibi": "He was working on another car."
            },
            "A Distracted Driver": {
                "motive": "He was using his phone at the time.",
                "alibi": "He claims he was at the grocery store."
            },
            "A Teenager": {
                "motive": "He was running late for an event.",
                "alibi": "He says he was on a date."
            }
        },
        "solution": "A Distracted Driver."
    },
    "Case 24": {
        "scenario": "A local charity's funds were embezzled.",
        "clues": [
            {"type": "evidence", "text": "Bank statements showed unauthorized withdrawals."},
            {"type": "evidence", "text": "A computer log was deleted."},
            {"type": "witness", "text": "An employee saw someone in the office late at night."}
        ],
        "suspects": {
            "The Treasurer": {
                "motive": "He wanted to pay off personal debts.",
                "alibi": "He claims he was at a fundraiser."
            },
            "A Volunteer": {
                "motive": "She was unhappy with her role.",
                "alibi": "She was at home."
            },
            "The Charity Director": {
                "motive": "He wanted to cover up his own mismanagement.",
                "alibi": "He was traveling for business."
            }
        },
        "solution": "The Treasurer."
    },
    "Case 25": {
        "scenario": "A community leader was found dead during a town hall meeting.",
        "clues": [
            {"type": "evidence", "text": "There were signs of a struggle in the meeting room."},
            {"type": "evidence", "text": "A broken chair was found nearby."},
            {"type": "witness", "text": "A participant heard shouting before the meeting started."}
        ],
        "suspects": {
            "A Local Businessman": {
                "motive": "He was angry over a recent decision against his interests.",
                "alibi": "He claims he was speaking with constituents."
            },
            "A Fellow Community Leader": {
                "motive": "She was envious of his popularity.",
                "alibi": "She was giving a presentation."
            },
            "A Distraught Citizen": {
                "motive": "He was unhappy with local policies.",
                "alibi": "He was in the back of the room."
            }
        },
        "solution": "A Local Businessman."
    }
}

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Could not request results; check your internet connection.")
            return ""

def present_case(case_name):
    case = cases[case_name]
    speak(f"Welcome to {case_name}.")
    speak(case["scenario"])
    
    for clue in case["clues"]:
        speak(f"Clue: {clue['text']}")
    
    speak("Would you like to know about the suspects, ask for a hint, or make an accusation?")

    points = 0
    while True:
        choice = listen()
        if "suspects" in choice:
            speak("Here are the suspects:")
            for suspect, details in case["suspects"].items():
                speak(f"{suspect}: {details['motive']}")
                speak(f"Alibi: {details['alibi']}")
            speak("Would you like to make an accusation or ask for a hint?")
        elif "hint" in choice:
            hint = random.choice(case["clues"])
            speak(f"Hint: {hint['text']}")
            points += 1  # Earn points for asking hints
            speak("You earned a point for asking a hint!")
        elif "accusation" in choice:
            speak("Who do you accuse?")
            accusation = listen()
            if accusation in case["suspects"]:
                speak("You accused " + accusation + ".")
                if accusation == case["solution"]:
                    speak("Congratulations! You solved the case!")
                    points += 5  # Earn points for solving the case
                    break
                else:
                    speak("That's incorrect. Try again.")
            else:
                speak("That suspect is not in this case. Please name a valid suspect.")
        else:
            speak("I didn't catch that. Please choose to know about the suspects, ask for a hint, or make an accusation.")

# Start the game
speak("Welcome to the Murder Mystery Game! Please say the name of the case you want to solve.")
case_names = list(cases.keys())
case_choice = listen()
if case_choice in case_names:
    present_case(case_choice)
else:
    speak("That case is not available. Please choose a valid case.")
