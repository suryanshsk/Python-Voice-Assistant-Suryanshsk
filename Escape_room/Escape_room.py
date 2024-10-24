import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
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
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you please repeat?")
            return listen()
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the service.")
            return None

def room(level):
    themes_and_riddles = [
        ("Room 1: The Echo of Time - I am heard yet unseen, whispering tales of ages gone by. What am I?", "memory"),
        ("Room 2: The Dancing Flames - I consume and illuminate, yet my touch brings both warmth and destruction. What am I?", "fire"),
        ("Room 3: The Invisible Thread - I connect hearts and minds, yet can be severed without a sound. What is it?", "trust"),
        ("Room 4: The Eternal Stream - I flow without form, shaping destinies in my wake. What am I?", "river"),
        ("Room 5: The Distant Glimmer - I shine bright yet elude grasp, a guide for dreamers lost in the night. What am I?", "star"),
        ("Room 6: The Veiled Secrets - I hold unspoken truths within, a silence that echoes louder than words. What is it?", "silence"),
        ("Room 7: The Luminous Path - I reveal journeys untold, yet am bound to remain just beyond reach. What could I be?", "light"),
        ("Room 8: The Enigmatic Vault - I hold keys to endless treasures yet remain locked within confines. What am I?", "knowledge"),
        ("Room 9: The Whispering Thoughts - I shape the world without form, a powerful force invisible to the eye. What is it?", "thought"),
        ("Room 10: The Life Current - I am the unseen force that drives all, felt but never held. What could I be?", "energy"),
        ("Room 11: The Forge of Dreams - From raw ideas, I create, melding potential into existence. What is it?", "imagination"),
        ("Room 12: The Heart's Tide - I ebb and flow, a spectrum of feelings that shape our very essence. What am I?", "emotion"),
        ("Room 13: The Soundscape - I vibrate through the air, stirring souls without uttering a word. What is it?", "music"),
        ("Room 14: The Ancient Library - I hold the wisdom of ages, guiding the lost without a visible path. What is it?", "wisdom"),
        ("Room 15: The Enigma of Shadows - I obscure truths and reveal mysteries, forever dancing in the dark. What am I?", "darkness"),
        ("Room 16: The Spark of Insight - I ignite the mind's canvas, a fleeting moment of clarity. What is it?", "idea"),
        ("Room 17: The Cycle of Ashes - I rise and fall, consuming all yet leaving behind the essence. What am I?", "fire"),
        ("Room 18: The Tower of Thoughts - I am a structure of ideas, ever-evolving yet immaterial. What could I be?", "thought"),
        ("Room 19: The Trail of Memories - I connect past to present, a journey that never truly fades. What am I?", "memory"),
        ("Room 20: The Realm of Justice - I exist without form, governed by principles that bind all. What am I?", "law"),
        ("Room 21: The Spectrum of Ideas - I flourish in the abstract, where potential is limitless. What is it?", "idea"),
        ("Room 22: The Dreamer's Atelier - I blend realities, crafting visions from the depths of imagination. What am I?", "dream"),
        ("Room 23: The Echoing Vault - I capture whispers of the past, shaping identities unseen. What is it?", "memory"),
        ("Room 24: The Creative Workshop - I transform thoughts into reality, an unseen realm of possibilities. What could it be?", "idea"),
        ("Room 25: The Reflected Pool - I foster deep contemplation, where ideas linger without form. What is it?", "thought"),
        ("Room 26: The Oasis of Insight - I converge knowledge, a guiding light through confusion. What am I?", "wisdom"),
        ("Room 27: The Sanctuary of Hearts - I cradle emotions, both joyous and painful, in my embrace. What is it?", "heart"),
        ("Room 28: The Workshop of Wonders - I am boundless creativity, forever expanding in imagination. What could it be?", "idea"),
        ("Room 29: The Garden of Thoughts - I nurture ideas to bloom, seen yet elusive. What is it?", "thought"),
        ("Room 30: The Canvas of Dreams - I am a void of potential, awaiting the brush of imagination. What could it be?", "imagination"),
        ("Room 31: The Weight of Possibilities - I carry unseen burdens, a presence felt deeply yet unnoticed. What could it be?", "thought"),
        ("Room 32: The Flow of Moments - I shape experiences into memories, a river of time unending. What am I?", "time"),
        ("Room 33: The Pathless Journey - I invite exploration, a voyage without beginning or end. What am I?", "line"),
        ("Room 34: The Beacon of Clarity - I illuminate the way, inspiring vision in the darkest hours. What could it be?", "vision"),
        ("Room 35: The Timeless Capsule - I preserve fleeting moments, echoing through eternity. What is it?", "time"),
        ("Room 36: The Force of Affection - I can unite or divide, a powerful influence in the realm of hearts. What is it?", "love"),
        ("Room 37: The Conception Lab - I am a hub of creativity, where ideas buzz with potential. What could it be?", "idea"),
        ("Room 38: The Hidden Knowledge - I am a vast repository, waiting for the seeker to unveil my secrets. What am I?", "knowledge"),
        ("Room 39: The Path of Contemplation - I guide the mind through uncharted territories, leading to insight. What is it?", "thought"),
        ("Room 40: The Abode of Understanding - I am a place where knowledge flourishes, enlightening all who seek. What is it?", "knowledge"),
        ("Room 41: The Emotional Spectrum - I shift like tides, a range of feelings waiting to be explored. What could it be?", "emotion"),
        ("Room 42: The Archive of the Past - I hold reflections that shape the identity of beings. What is it?", "memory"),
        ("Room 43: The Clarity Haven - I align scattered thoughts, revealing hidden insights. What could it be?", "thought"),
        ("Room 44: The Seeker of Truth - I resonate in silence, unveiling what lies beneath. What is it?", "truth"),
        ("Room 45: The Nexus of Connections - I bind lives and experiences, a force without chains. What could it be?", "relationship"),
        ("Room 46: The Sphere of Ideas - I expand creativity, soaring to heights unknown. What is it?", "imagination"),
        ("Room 47: The Essence of Existence - I am the core shaped by experience, ever whole yet complex. What am I?", "identity"),
        ("Room 48: The Guiding Light - I offer hope in darkness, a presence often felt yet rarely seen. What is it?", "hope"),
        ("Room 49: The Shifting Paradigm - I am the ever-evolving essence of thought and understanding. What could I be?", "idea"),
        ("Room 50: The Final Puzzle - I am a riddle wrapped in a mystery, the key to unlocking all realms. What am I?", "life"),
    ]

    if level <= len(themes_and_riddles):
        theme_riddle, answer = themes_and_riddles[level - 1]
        speak(theme_riddle)

        while True:
            user_answer = listen()
            if user_answer == answer:
                speak("Correct! You've escaped this room.")
                return True
            else:
                speak("That's not correct. Try again.")

def boss_level():
    speak("Welcome to the Boss Level! Solve this riddle to claim your victory.")
    speak("I am formless yet present in the skies and seas, a guide for the lost and a cradle for dreams. What am I?")
    answer = "cloud"

    while True:
        user_answer = listen()
        if user_answer == answer:
            speak("Correct! You have defeated the boss and claimed your victory!")
            speak("Congratulations! You are now a master of the escape room!")
            return True
        else:
            speak("That's not correct. Try again.")

def main():
    speak("Welcome to the Voice-Powered Escape Room!")
    for level in range(1, 51):
        if not room(level):
            speak("Thanks for playing!")
            return
    boss_level()

if __name__ == "__main__":
    main()