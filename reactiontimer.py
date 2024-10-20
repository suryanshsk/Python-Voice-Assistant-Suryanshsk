import tkinter as tk
import random
import time
from tkinter import messagebox

class ReactionTimerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Timer: Color Change")
        self.root.geometry("400x200")

        self.label = tk.Label(self.root, text="Wait for the button to turn green...", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.button = tk.Button(self.root, text="Click Me!", bg="gray", font=("Helvetica", 14), width=20, height=2, state=tk.DISABLED)
        self.button.pack(pady=20)
        self.button.bind("<Button-1>", self.check_reaction)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game, font=("Helvetica", 14), width=10)
        self.start_button.pack(pady=20)

        self.start_time = 0
        self.is_ready = False

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        self.label.config(text="Get Ready...")
        self.button.config(bg="gray", state=tk.DISABLED)

        delay = random.uniform(2, 5)  # Random delay between 2 and 5 seconds
        self.root.after(int(delay * 1000), self.activate_button)

    def activate_button(self):
        self.button.config(bg="green", state=tk.NORMAL)
        self.label.config(text="Click now!")
        self.start_time = time.time()
        self.is_ready = True

    def check_reaction(self, event):
        if self.is_ready:
            reaction_time = time.time() - self.start_time
            self.is_ready = False
            messagebox.showinfo("Reaction Time", f"Your reaction time: {reaction_time:.3f} seconds")
        else:
            messagebox.showwarning("Too Soon!", "You clicked too soon!")

        self.reset_game()

    def reset_game(self):
        self.button.config(bg="gray", state=tk.DISABLED)
        self.label.config(text="Wait for the button to turn green...")
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = ReactionTimerGame(root)
    root.mainloop()
