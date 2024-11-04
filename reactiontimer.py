import tkinter as tk
import random
import time
from tkinter import messagebox

class ReactionTimerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Timer: Color Change")
        self.root.geometry("600x400")

        self.label = tk.Label(self.root, text="Wait for the button to turn green...", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.button = tk.Button(self.root, text="Click Me!", bg="gray", font=("Helvetica", 14), width=20, height=2, state=tk.DISABLED)
        self.button.pack(pady=20)
        self.button.bind("<Button-1>", self.check_reaction)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game, font=("Helvetica", 14), width=10)
        self.start_button.pack(pady=20)
        
        #display for high score and history
        self.high_score = float('inf')
        self.high_score_label = tk.Label(self.root, text="High Score: N/A", font=("Helvetica", 12))
        self.high_score_label.pack(pady=10)
        
        self.history = []
        self.history_label = tk.Label(self.root, text="Reaction Times", font=("Helvetica", 12))
        self.high_score_label.pack(pady=10)
        
        #Difficulty level selection
        self.difficulty = tk.StringVar(value="Medium")
        tk.Label(self.root, text="Difficulty level:", font=("Helvetica", 12)).pack()
        tk.OptionMenu(self.root, self.difficulty, "Easy", "Medium", "Hard").pack(pady=10)
        
        self.start_time = 0
        self.is_ready = False

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        self.label.config(text="Get Ready...")
        self.button.config(bg="gray", state=tk.DISABLED)
        
        #set delay based on difficulty level
        if self.difficulty.get() == "Easy":
            delay = random.uniform(2, 5)
        elif self.difficulty.get() == "Medium":
            delay = random.uniform(1.5, 3)
        else:
            delay = random.unifrom(1, 2)
            
        #start the timer for the button to turn green
        self.root.after(int(delay*1000), self.activate_button)


    def activate_button(self):
        #randomize button position
        x = random.randint(50, self.root.winfo_width() - 150)
        y = random.randint(50, self.root.winfo_height() - 150)
        self.button.place(x=x, y=y)
        
        #activate button and start reaction time
        self.button.config(bg="green", state=tk.NORMAL)
        self.label.config(text="click now!")
        self.start_time = time.time()
        self.is_ready = True
    
        
    def check_reaction(self, event):
        if self.is_ready:
            reaction_time = time.time() - self.start_time
            self.is_ready = False

            # Add reaction time to history and update display
            self.history.append(reaction_time)
            if len(self.history) > 5:
                self.history.pop(0)
            self.history_label.config(text="Reaction Times: " + ", ".join(f"{t:.3f}" for t in self.history))

            # Check for high score
            if reaction_time < self.high_score:
                self.high_score = reaction_time
                self.high_score_label.config(text=f"High Score: {self.high_score:.3f} seconds")
                messagebox.showinfo("New High Score!", f"New high score: {self.high_score:.3f} seconds")

            # Provide feedback based on performance
            if reaction_time < 0.3:
                feedback = "Excellent!"
            elif reaction_time < 0.5:
                feedback = "Good!"
            else:
                feedback = "Try Again!"
            messagebox.showinfo("Reaction Time", f"{feedback} Your reaction time: {reaction_time:.3f} seconds")
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
