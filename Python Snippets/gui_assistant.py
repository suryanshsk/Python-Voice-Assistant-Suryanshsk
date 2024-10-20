import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Voice Assistant GUI")
root.geometry("600x400")

# Load and display an image
image_path = "sound_wave.png"
image = Image.open(image_path)
image = image.resize((400, 100), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)

label = tk.Label(root, image=photo)
label.pack(pady=20)

# Create a function to trigger voice assistant
def start_assistant():
    # Here you can integrate with your voice assistant functionality
    # For example, call the main function from your voice assistant
    print("Voice Assistant Started...")

# Create a button to start the assistant
start_button = tk.Button(root, text="Start Voice Assistant", command=start_assistant)
start_button.pack(pady=20)

root.mainloop()
