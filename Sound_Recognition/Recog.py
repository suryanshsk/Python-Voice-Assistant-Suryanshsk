import sounddevice as sd
import numpy as np
import pyttsx3
import speech_recognition as sr
import json
import os
from threading import Thread

class SoundAssistant:
    def __init__(self, sound_file='sounds.json'):
        self.engine = pyttsx3.init()
        self.sounds_to_listen_for = self.load_sounds(sound_file)
        self.sound_file = sound_file
        self.recognizer = sr.Recognizer()
        self.is_listening = True

    def load_sounds(self, sound_file):
        if os.path.exists(sound_file):
            with open(sound_file, 'r') as f:
                return json.load(f)
        return []

    def save_sounds(self):
        with open(self.sound_file, 'w') as f:
            json.dump(self.sounds_to_listen_for, f)

    def update_sounds(self, new_sounds):
        self.sounds_to_listen_for.extend(new_sounds)
        self.sounds_to_listen_for = list(set(self.sounds_to_listen_for))
        self.save_sounds()
        self.speak(f"Now listening for: {', '.join(self.sounds_to_listen_for)}", whisper=False)

    def sound_callback(self, indata, frames, time, status):
        if status:
            print(status)
        audio_data = np.frombuffer(indata, dtype=np.float32)
        detected_sound = self.detect_sound(audio_data)
        if detected_sound:
            self.handle_sound(detected_sound)

    def detect_sound(self, audio_data):
        if np.mean(audio_data) > 0.1:
            return "random_sound"
        return None

    def handle_sound(self, detected_sound):
        if detected_sound in self.sounds_to_listen_for:
            print(f"Detected sound: {detected_sound}")
            self.speak(f"I heard a {detected_sound}!", whisper=True)

    def speak(self, text, whisper=False):
        if whisper:
            self.engine.setProperty('volume', 0.2)
        else:
            self.engine.setProperty('volume', 1.0)
        
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.setProperty('volume', 1.0)

    def listen(self):
        with sd.InputStream(callback=self.sound_callback):
            print("Listening for sounds...")
            while self.is_listening:
                sd.sleep(100)

    def listen_for_phrases(self):
        while True:
            with sr.Microphone() as source:
                print("Speak the sounds you want to listen for, or say 'stop listening' to end:")
                audio = self.recognizer.listen(source)
                try:
                    user_input = self.recognizer.recognize_google(audio).lower()
                    if "stop listening" in user_input:
                        print("Stopping sound detection.")
                        self.is_listening = False
                        self.speak("Sound detection has been stopped.", whisper=False)
                        break
                    new_sounds = user_input.split(",")
                    self.update_sounds([sound.strip() for sound in new_sounds])
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service; {e}")

if __name__ == "__main__":
    assistant = SoundAssistant()
    listening_thread = Thread(target=assistant.listen)
    listening_thread.start()
    assistant.listen_for_phrases()
