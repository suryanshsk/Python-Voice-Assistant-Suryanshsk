import tkinter as tk
from PIL import Image, ImageTk, ImageOps

root = tk.Tk()
root.title("Voice Assistant GUI")
root.geometry("600x400")
image_path = "sound_wave.png"
image = Image.open(image_path)
image = image.resize((400, 100), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)
label = tk.Label(root, image=photo)
label.pack(pady=20)
root.mainloop()
