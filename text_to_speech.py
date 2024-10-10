from gtts import gTTS
import os
import platform

# Taking input from the user
text = input("Enter the text you want to convert to speech: ")

# Specifying the language for conversion
language = 'en'

# Creating the gTTS object and converting the text
speech = gTTS(text=text, lang=language, slow=False)

# Saving the speech to an mp3 file
filename = "user_output.mp3"
speech.save(filename)

# Detect the OS and play the mp3 file accordingly
os_type = platform.system()

if os_type == "Windows":
    os.system(f"start {filename}")
elif os_type == "Darwin":  # macOS
    os.system(f"afplay {filename}")
else:  # Linux
    os.system(f"mpg321 {filename}")  # mpg321 should be installed on Linux
