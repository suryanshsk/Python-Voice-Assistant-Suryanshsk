import speech_recognition as sr
import pyttsx3
import re

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            response = recognizer.recognize_google(audio)
            print(f"You said: {response}")
            return response.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return ""

def ask_question(question, options):
    speak(question)
    response = listen()
    normalized_response = normalize_response(response)
    
    for key in options.keys():
        if key in normalized_response:
            return options[key]
    
    print("Response not recognized. Please answer clearly.")
    return ask_question(question, options)  # Retry asking the question

def normalize_response(response):
    # Normalize the response to handle different expressions
    if response:
        return re.sub(r'\W+', ' ', response).strip()
    return ""

def personality_test():
    questions = [
        ("After a long week, do you prefer to recharge by going out with friends or having a quiet night in?", {"going out": "E", "quiet night": "I"}),
        ("Would you rather host a party or attend one?", {"host": "E", "attend": "I"}),
        ("When faced with a problem, do you first consider logical aspects or emotional impacts?", {"logical": "T", "emotional": "F"}),
        ("Do you find it easier to remember facts or concepts?", {"facts": "S", "concepts": "N"}),
        ("When starting a new project, do you prefer to dive right in or create a detailed plan?", {"dive in": "P", "detailed plan": "J"}),
        ("Do you prefer working on one task at a time or juggling multiple tasks?", {"one task": "J", "multiple tasks": "P"}),
        ("Do you feel comfortable in large groups or do you prefer small gatherings?", {"large groups": "E", "small gatherings": "I"}),
        ("Are you more likely to express your opinions openly or keep them to yourself?", {"express": "E", "keep to self": "I"}),
        ("How do you react to unexpected changes in your plans?", {"adapt easily": "E", "feel stressed": "S"}),
        ("Do you thrive on routine or prefer flexibility?", {"routine": "J", "flexibility": "P"}),
        ("Do you tend to empathize more or stick to objective reasoning?", {"empathize": "F", "objective": "T"}),
        ("In emotional situations, do you prefer to talk it out or take time to think?", {"talk it out": "E", "think": "I"}),
        ("Are you more likely to come up with new ideas or improve existing ones?", {"new ideas": "N", "improve": "S"}),
        ("Do you enjoy exploring abstract concepts or practical applications?", {"abstract": "N", "practical": "S"}),
        ("When making decisions, do you prioritize your own values or consider the impact on others?", {"own values": "T", "impact on others": "F"}),
        ("Do you believe rules are meant to be followed or interpreted?", {"followed": "J", "interpreted": "P"}),
        ("Do you prefer spending your free time on hobbies or socializing?", {"hobbies": "I", "socializing": "E"}),
        ("Would you rather watch a documentary or a comedy?", {"documentary": "N", "comedy": "S"}),
        ("Do you tend to think about long-term implications or focus on immediate benefits?", {"long-term": "J", "immediate": "P"}),
        ("Are you more driven by achieving goals or enjoying the journey?", {"achieving goals": "T", "enjoying journey": "F"}),

        # New questions
        ("Do you prefer deep conversations or casual chit-chat?", {"deep conversations": "I", "casual chit-chat": "E"}),
        ("When making a decision, do you rely more on your gut feeling or thorough analysis?", {"gut feeling": "F", "thorough analysis": "T"}),
        ("Do you prefer hands-on learning experiences or theoretical discussions?", {"hands-on": "S", "theoretical": "N"}),
        ("In a conflict, do you prefer to address it directly or let it resolve naturally?", {"address directly": "E", "let it resolve": "I"}),
        ("Do you thrive in creative environments or structured ones?", {"creative": "N", "structured": "J"}),
        ("Do you focus more on the present moment or think about future possibilities?", {"present moment": "S", "future possibilities": "N"}),
        ("How do you feel about ambiguity: do you embrace it or prefer clear answers?", {"embrace it": "P", "prefer clear answers": "J"}),
        ("When under stress, do you seek social support or prefer to handle it alone?", {"social support": "E", "handle alone": "I"}),
        ("Are you more motivated by personal achievements or external recognition?", {"personal achievements": "I", "external recognition": "E"}),
        ("Do you gravitate towards people-oriented activities or task-oriented ones?", {"people-oriented": "E", "task-oriented": "I"}),
    ]

    scores = {"I": 0, "E": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for question, options in questions:
        response = ask_question(question, options)
        if response:
            scores[response] += 1

    return scores

def determine_personality(scores):
    personality = ""
    personality += "I" if scores["I"] > scores["E"] else "E"
    personality += "S" if scores["S"] > scores["N"] else "N"
    personality += "T" if scores["T"] > scores["F"] else "F"
    personality += "J" if scores["J"] > scores["P"] else "P"
    return personality

def personality_feedback(personality):
    personality_types = {
        "INTJ": "The Architect: Innovative, independent, and strategic. They often see the big picture and are focused on their goals.",
        "INTP": "The Thinker: Analytical and open-minded, they enjoy exploring new ideas and theories.",
        "ENTJ": "The Commander: Natural leaders who are efficient and goal-oriented.",
        "ENTP": "The Debater: Quick-witted and enthusiastic, they thrive on challenges.",
        "ISFJ": "The Defender: Supportive and reliable, they are very detail-oriented.",
        "ISFP": "The Artist: Creative and adaptable, they enjoy expressing themselves.",
        "ESFJ": "The Provider: Warm and organized, they are often very conscientious.",
        "ESFP": "The Performer: Energetic and fun-loving, they thrive in social settings.",
        "INFJ": "The Advocate: Insightful and inspiring, they seek to make a positive impact.",
        "INFP": "The Mediator: Idealistic and empathetic, they value authenticity.",
        "ENFJ": "The Protagonist: Charismatic and driven, they are often seen as natural leaders.",
        "ENFP": "The Campaigner: Enthusiastic and creative, they are great at motivating others.",
        "ISTJ": "The Logistician: Responsible and practical, they value tradition and order.",
        "ISXX": "The Observer: Detail-oriented and observant.",
        "ESTJ": "The Executive: Efficient and organized, they are often seen as natural leaders.",
        "ESTP": "The Entrepreneur: Energetic and action-oriented, they love challenges.",
    }

    return personality_types.get(personality, "Unknown personality type.")

def main():
    speak("Welcome to the advanced personality type test.")
    scores = personality_test()
    personality = determine_personality(scores)
    result = personality_feedback(personality)
    speak(f"Your personality type is: {personality}. {result}")

if __name__ == "__main__":
    main()
