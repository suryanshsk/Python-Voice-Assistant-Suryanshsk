## **Crisis support feature**

### 🎯 **Goal**

The goal of this project is to create a crisis support feature that operates via voice commands.

### 🧾 **Description**

This feature provides crisis support to the user. It can:
1. Recognize Crisis-Related Commands
2. Provide Immediate Support
3. Offer Crisis Helplines
4. Connect to Crisis Resources

### 🧮 **Features:**

Built a program that offers the following features:

1. Voice Recognition:
The assistant captures audio input from the user and converts it to text using the speech_recognition library.

2. Crisis Detection:
The program uses a list of crisis-related keywords and phrases to identify when a user may be in distress. It also analyzes the sentiment of the user's spoken input to gauge emotional severity using the textblob library.
 
3. Fuzzy Matching:
It employs fuzzy string matching with the fuzzywuzzy library to detect variations of crisis-related phrases, making the assistant more robust in understanding user input.

4. Helpline Information:
Depending on the user's location (US, UK, India, or global), the assistant provides specific helplines for mental health support, including general, text support, and emergency contacts.

The assistant continuously listens for commands and provides responses, allowing users to exit the session by saying "exit" or "stop."

### 📚 **Libraries Needed**

1. `speech_recognition` : For voice input (speech-to-text).
2. `pyttsx3` : For voice output (text-to-speech).
3. `fuzzywuzzy` : For detecting similar phrases with fuzzy matching.
4. `textblob` : For sentiment analysis to detect crisis-related emotions.


### 📢 **Conclusion**

The crisis support feature aims to create a safe and responsive environment for users seeking help, leveraging voice technology to facilitate access to mental health resources.
