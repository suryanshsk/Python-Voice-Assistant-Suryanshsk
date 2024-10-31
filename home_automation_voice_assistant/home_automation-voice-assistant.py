import paho.mqtt.client as mqtt
import speech_recognition as sr
import pyttsx3
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import time
import random
import re
from datetime import datetime, timedelta
import threading

# Initialize Text-to-Speech Engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

# Load stopwords for NLP processing
try:
    stop_words = set(stopwords.words("english"))
except:
    import nltk
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
nltk.download('punkt')

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "home/automation"

# Device Configuration (Loaded from JSON for easy expansion)
with open("devices.json", "r") as f:
    DEVICES = json.load(f)

# Initialize MQTT Client
mqtt_client = mqtt.Client()
connected = False

# Device State Management
device_states = {device: "off" for device in DEVICES}

# MQTT Connection Functions
def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print("Connected to MQTT Broker!")
        connected = True
    else:
        print(f"Failed to connect, return code {rc}")
        connected = False

def on_disconnect(client, userdata, rc):
    global connected
    print("Disconnected from MQTT Broker")
    connected = False
    reconnect()

def reconnect():
    global connected
    while not connected:
        try:
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            mqtt_client.loop_start()
            connected = True
        except:
            print("Reconnection attempt failed. Trying again in 5 seconds...")
            time.sleep(5)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Advanced Command Parsing with Context
def process_command(command):
    command = command.lower()
    words = word_tokenize(command)
    filtered_words = [word for word in words if word not in stop_words]

    found_device = None
    found_action = None
    scheduled_time = None

    # Recognize devices and actions
    for device, actions in DEVICES.items():
        if device in filtered_words:
            found_device = device
            for action in actions:
                if action in command:
                    found_action = action
                    break
            break

    # Detect scheduled commands (e.g., "in 10 minutes")
    time_match = re.search(r"in (\d+) (minute|minutes|hour|hours)", command)
    if time_match:
        time_value = int(time_match.group(1))
        time_unit = time_match.group(2)
        scheduled_time = datetime.now() + timedelta(minutes=time_value) if "minute" in time_unit else datetime.now() + timedelta(hours=time_value)

    # Execute or schedule the command
    if found_device and found_action:
        if scheduled_time:
            schedule_command(found_device, found_action, scheduled_time)
        else:
            execute_command(found_device, found_action)
    else:
        respond("Sorry, I didn't understand the command. Please try again.")

# Command Execution
def execute_command(device, action):
    if device_states[device] == action:
        respond(f"The {device} is already {action}.")
    else:
        device_states[device] = action
        publish_mqtt(device, action)
        respond(f"{device.capitalize()} is now set to {action}.")

# Schedule a Command for Later
def schedule_command(device, action, scheduled_time):
    delay = (scheduled_time - datetime.now()).total_seconds()
    threading.Timer(delay, execute_command, args=(device, action)).start()
    respond(f"{device.capitalize()} will be set to {action} at {scheduled_time.strftime('%H:%M')}.")

# Publish MQTT Messages
def publish_mqtt(device, action):
    topic = f"{MQTT_TOPIC_PREFIX}/{device}"
    mqtt_client.publish(topic, action)
    print(f"Sent '{action}' command to {device}.")

# Text-to-Speech Feedback
def respond(message):
    print(message)
    tts_engine.say(message)
    tts_engine.runAndWait()

# Voice Recognition with retry mechanism
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: '{command}'")
            process_command(command)
        except sr.UnknownValueError:
            respond("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            respond("Could not request results; check your internet connection.")

# Main loop
if __name__ == "__main__":
    print("Advanced Home Automation Controller is running...")
    try:
        while True:
            if connected:
                listen_for_command()
            else:
                reconnect()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
