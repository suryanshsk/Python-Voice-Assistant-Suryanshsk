# 🔊 Home Automation Voice Assistant

> An AI-powered voice assistant for home automation, with features like context-aware commands, scheduling, real-time device state management, and flexible device configuration.

---

## 🌟 Features

- **Enhanced Natural Language Processing (NLP):** Understands commands intuitively, even with varying phrases.
- **Context-Aware Commands:** Controls multiple devices in a single command.
- **Scheduled Actions:** Automate your devices on a delay or schedule.
- **Real-Time Device State Feedback:** Keeps track of each device's state and responds accordingly.
- **Easy Device Expansion:** Add new devices and actions via a JSON configuration file.
- **Voice Feedback:** Confirms actions with text-to-speech.

---

## 📋 Requirements

- **Python**: >= 3.7
- **Libraries**: Install using the requirements file
- **MQTT Broker**: [HiveMQ](https://www.hivemq.com/) (or your choice of MQTT broker)
- **Microphone**: For voice input

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dino65-dev/Home_automation-voice-assistant.git
   cd home_automation-voice-assistant
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Edit the Device Configuration: Update ```devices.json``` to add or modify devices and actions.**
   ```json
   {
    "lights": ["on", "off", "dim", "brighten"],
    "fan": ["on", "off", "speed up", "slow down"],
    "tv": ["on", "off", "volume up", "volume down"],
    "ac": ["on", "off", "temperature up", "temperature down"],
    "curtains": ["open", "close"]
   }
   ```
4. **Configure the MQTT Broker: Edit the ```MQTT_BROKER``` and ```MQTT_PORT``` values in the code to point to your MQTT broker.**
5. **Run the voice assistant:**
   ```bash
   python home_automation-voice-assistant.py
---
### 🔧 Usage
This assistant listens for voice commands to control home automation devices. It recognizes various commands for different devices based on the configuration in ```devices.json```.

**Available Commands**
1. **Basic Commands:**
- "Turn on the lights."
- "Switch off the fan."
- "Set the AC to temperature up."

2. **Multi-Device Commands:**
- "Turn off the lights and fan."
- "Set TV to volume up and AC to temperature down."
  
3. **Scheduled Commands:**
- "Turn on the lights in 10 minutes."
- "Switch off the fan in 1 hour."
---
### 🎛️ Advanced Features
1. **Scheduling:**
- Commands like "Turn off the lights in 5 minutes" will execute with a delay.
2. **State Awareness:**
- Responds with messages like "The lights are already on" if you try to turn on a device that’s already active.
3. **Extensible Configuration:**
- Easily add new devices or actions without modifying the code. Just update ```devices.json```!
4. **Interactive Feedback:**
- The assistant provides voice feedback after each command, confirming the action.
---
### 🛠 Troubleshooting
1. **Issue with Voice Recognition?**
- Make sure your microphone is connected and set as the default recording device.
- Speak clearly and check for ambient noise that may interfere.
2. **Error Connecting to MQTT?**
- Double-check the ```MQTT_BROKER``` and ```MQTT_PORT```.
- Ensure your MQTT broker is running and accessible.
3. **New Device Not Recognized?**
- Ensure the device and its actions are correctly added to ```devices.json```.
- Restart the program after making changes to the configuration.
---
## 📖 Commands Overview

| Command Example                          | Description                                    |
|------------------------------------------|------------------------------------------------|
| `Turn on the lights`                    | Activates the lights                           |
| `Switch off the fan`                    | Deactivates the fan                            |
| `Turn on the AC in 10 minutes`          | Schedules the AC to turn on after 10 minutes   |
| `Set TV to volume down and AC to off`   | Controls multiple devices in one command       |
| `Increase heater temperature`            | Increases heater setting (custom actions)      |

---
## 📦 Extending the System

You can expand the system by editing `devices.json`. Each device can have unique actions. Just add entries for each device and action in JSON format:

```json
{
    "smart_light": ["on", "off", "dim", "brighten"],
    "smart_blinds": ["open", "close", "adjust"]
}
```
---
## 🧩 Contributing

Feel free to contribute to this project! Open an issue or submit a pull request to suggest or implement new features.

---

## 🎉 Final Tips

1. **Clear Commands**: Try to give clear and distinct commands.
2. **Add Custom Responses**: Customize `respond()` function in the code for unique voice responses.
3. **Experiment with Scheduling**: Test different scheduled times to see how the assistant handles delays.
---
## ✨ Created by Dinmay Brahma
**Star ⭐ the repository if you found this project helpful!**

> _Automate your home with your voice and experience the power of an intelligent assistant!_


---

Feel free to add more information or edit it to match the specifics of your project. This README template is designed to be visually appealing, easy to navigate, and informative for users on GitHub. Let me know if you’d like further customization!


