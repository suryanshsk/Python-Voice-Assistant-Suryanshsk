# SoundBuddy

## Overview

SoundBuddy is a Python-powered assistant that listens for specific sounds and responds to user-defined phrases with voice feedback. It seamlessly blends audio detection and speech recognition for a fun, interactive experience.

## What I’ve Done

SoundBuddy allows users to customize the sounds it monitors. Key features include:

- Real-time audio input listening.
- Detection of user-defined sounds.
- Friendly voice responses when sounds are recognized.
- Easy updates to monitored sounds via speech.

## Libraries Imported
- sounddevice: Captures audio input.
- numpy: Processes audio data.
- pyttsx3: Converts text to speech.
- speech_recognition: Recognizes spoken phrases.
- json: Manages sound configurations.
- os: Handles file operations.
- threading: Enables concurrent listening processes.

## What This Code Does
- Initialization: Sets up text-to-speech and loads sounds from a JSON file.
- Sound Detection: Listens for audio input and detects sounds based on a threshold.
- Voice Feedback: Provides verbal confirmation when a sound is detected.
- User Interaction: Allows users to define sounds through speech and stop the assistant with a command.
- Threading: Runs sound detection and speech recognition simultaneously.

## Conclusion
SoundBuddy demonstrates the potential of Python in creating engaging audio applications, offering a solid foundation for future enhancements in sound detection and user interaction. Get ready to chat with your sounds!