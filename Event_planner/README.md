# Voice Event Planner

## Overview
Voice Event Planner is a simple voice-activated assistant designed to help users manage their events. With intuitive voice commands, users can easily add and list events, making event planning hassle-free and hands-free.

## What Have I Done
I developed a voice assistant using Python that leverages speech recognition and text-to-speech capabilities. The assistant can listen to user commands, interpret them, and manage a list of events stored in a JSON file. This project showcases the integration of voice technology with practical application development.

## Libraries
This project uses the following libraries:
- `speech_recognition`: For converting spoken language into text.
- `pyttsx3`: For converting text back into speech.
- `datetime`: For handling date and time.
- `json`: For reading and writing event data.
- `os`: For interacting with the operating system.
- `dateutil`: For parsing dates in a flexible manner.

## What This Code Does
- **Listen for Commands**: The assistant listens for user commands through the microphone.
- **Add Events**: Users can add events by providing the event name and date.
- **List Events**: Users can view a list of their upcoming events.
- **Exit Confirmation**: Before exiting, the assistant asks for user confirmation to ensure no accidental exits occur.

## Conclusion
Voice Event Planner is a practical demonstration of how voice recognition technology can enhance user experience in everyday tasks. By integrating speech processing with event management, this assistant offers a user-friendly solution for organizing important dates. 