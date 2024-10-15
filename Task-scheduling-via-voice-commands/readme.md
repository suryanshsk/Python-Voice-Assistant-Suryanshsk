# Task Scheduler via Voice Commands

This repository contains a **Task Scheduling** feature via **Voice Commands**, developed as part of the **Cognova** voice assistant. It allows users to schedule tasks or set reminders by speaking to the assistant, such as:  
> "Remind me to attend a meeting at 2 PM."

The assistant will then acknowledge the task and schedule a reminder that will be triggered at the specified time. The feature is implemented using Python with `SpeechRecognition`, `pyttsx3` (for text-to-speech), and `apscheduler` (for scheduling tasks).

## Features
- **Voice-activated task scheduling:** Schedule tasks or set reminders by speaking to the assistant.
- **Text-to-speech functionality:** The assistant responds verbally to user input.
- **Real-time scheduling:** Set reminders for tasks at specific times (e.g., "Remind me to attend a meeting at 2 PM").
- **Speech recognition:** Captures user commands using speech-to-text.
- **Interactive assistant:** The assistant listens for commands and provides feedback.

## Technology Stack
- **Python 3.x**
- **SpeechRecognition** (for capturing voice input)
- **pyttsx3** (for text-to-speech conversion)
- **APScheduler** (for scheduling tasks/reminders)
- **GitHub Codespaces** (to run the project easily in the cloud)

## Setup and Installation

### Step 1: Clone the Repository
To get started, clone this repository to your local machine or GitHub Codespaces.

```bash
git clone https://github.com/your-username/voice-task-scheduler.git
cd voice-task-scheduler
```

### Step 2: Install Dependencies
Ensure that you have Python installed (Python 3.6+ recommended). Install the necessary Python libraries.

```bash
pip install speechrecognition pyttsx3 apscheduler
```

### Step 3: Run the Assistant
To start the voice assistant, simply run the `task_scheduler.py` script:

```bash
python task_scheduler.py
```

### Step 4: Interact with the Assistant
The assistant will greet you and start listening for commands. Example commands:

- **Set a Reminder:**  
  _"Remind me to attend a meeting at 2 PM"_

- **Exit the Assistant:**  
  _"Exit"_

### Step 5: Running on GitHub Codespaces
1. Open the repository in GitHub Codespaces by clicking on **Code** > **Open with Codespaces** in your repository.
2. Open the terminal in Codespaces.
3. Install dependencies as shown above.
4. Run the script as shown above.

### Notes:
- Ensure that your microphone is enabled if you're using GitHub Codespaces or a local machine.
- The project currently does not persist tasks between sessions (optional feature to add).

## Contributing
Contributions are welcome! Here’s how you can help improve this project:
1. **Fork the repository.**
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a **Pull Request**.

## Issues
If you encounter any issues with the voice task scheduler, feel free to open an issue on GitHub, and we will address it as soon as possible.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.