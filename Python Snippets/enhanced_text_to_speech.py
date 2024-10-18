import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.set_voice(0)  # Default to the first available voice
        self.set_rate(150)  # Default speech rate
        self.set_volume(1.0)  # Max volume

    def set_voice(self, voice_index):
        """Set the voice by index (0 for first voice, 1 for second, etc.)."""
        voices = self.engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
        else:
            print("Invalid voice index.")

    def set_rate(self, rate):
        """Set the speech rate."""
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """Set the volume (0.0 to 1.0)."""
        self.engine.setProperty('volume', volume)

    def speak(self, text):
        """Speak the given text."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during speech: {e}")
if __name__ == '__main__':
    tts = TextToSpeech()
    tts.speak("Hello, how can I assist you today?")
