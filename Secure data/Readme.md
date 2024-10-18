VoiceGuard: Your Secure Voice Assistant

🎯 Goal
The goal of this project is to create a voice assistant that securely stores sensitive information, such as messages, addresses, or codes, and allows retrieval only through user-defined security questions.

🧾 Description
VoiceGuard is a cutting-edge voice assistant that utilizes speech recognition and text-to-speech capabilities to help users manage their sensitive information. Users can store information along with custom security questions and retrieve it only after correctly answering those questions.

🧮 What I had done!

Built a voice interface using speech_recognition for user input and pyttsx3 for output.
Implemented functionality to securely store information using encryption with cryptography.fernet.
Allowed users to define their own security questions and answers when storing information.
Created a locking mechanism that restricts access after incorrect retrieval attempts, requiring the user to answer security questions to regain access.
Developed an interactive loop where users can continuously store, retrieve, or exit the assistant.
📚 Libraries Needed

speech_recognition - For recognizing user voice commands.
pyttsx3 - For converting text to speech for user interaction.
cryptography - To encrypt and decrypt sensitive information securely.
os - For handling file operations related to key management.
📢 Conclusion
In conclusion, VoiceGuard showcases fundamental programming concepts such as secure data handling, speech recognition, and user input management in Python. It provides a robust and engaging experience where users can store and access sensitive information securely. This project serves as an excellent learning opportunity for developers looking to enhance their understanding of Python and voice interaction.