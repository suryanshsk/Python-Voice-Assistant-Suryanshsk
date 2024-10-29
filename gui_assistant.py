import tkinter as tk
import math
import speech_recognition as sr
import threading

root = tk.Tk()
root.title("Voice Assistant GUI with Sound Wave")
root.geometry("600x400")

canvas = tk.Canvas(root, width=600, height=200, bg="white")
canvas.pack(pady=20)

amplitude = 80
frequency = 0.05
speed = 0.1
phase = 0 

def animate_wave():
    global phase
    canvas.delete("all") 

    width = 600  
    height = 100 

    for x in range(width):
        y = height + amplitude * math.sin(2 * math.pi * frequency * x + phase)
        canvas.create_line(x, height, x, y, fill="black")
    phase += speed
    canvas.after(20, animate_wave)

animate_wave()

def listen_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for your voice...")

        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Could not request results; check your network connection.")

def start_assistant():
    print("Voice Assistant Started...")
    threading.Thread(target=listen_voice).start()

start_button = tk.Button(root, text="Start Voice Assistant", command=start_assistant)
start_button.pack(pady=20)

root.mainloop()
