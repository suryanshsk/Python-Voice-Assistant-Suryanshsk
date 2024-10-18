import tkinter as tk
from tkinter import ttk
import random

# Function to determine the winner
def check_result(player_choice):
    options = ['Rock', 'Paper', 'Scissors']
    computer_choice = random.choice(options)
    
    if player_choice == computer_choice:
        result.set(f"Tie! Both chose {player_choice}")
    elif (player_choice == 'Rock' and computer_choice == 'Scissors') or \
         (player_choice == 'Paper' and computer_choice == 'Rock') or \
         (player_choice == 'Scissors' and computer_choice == 'Paper'):
        result.set(f"You win! {player_choice} beats {computer_choice}")
    else:
        result.set(f"You lose! {computer_choice} beats {player_choice}")

# Set up the main window
root = tk.Tk()
root.title("Rock-Paper-Scissors Game")
root.geometry("300x200")

# Dropdown menu for player's choice
player_choice = tk.StringVar()
choices = ['Rock', 'Paper', 'Scissors']
player_choice.set(choices[0])

ttk.Label(root, text="Choose:").pack(pady=10)
dropdown = ttk.OptionMenu(root, player_choice, *choices)
dropdown.pack()

# Button to play the game
play_button = ttk.Button(root, text="Play", command=lambda: check_result(player_choice.get()))
play_button.pack(pady=10)

# Result display
result = tk.StringVar()
result.set("Make your choice!")
ttk.Label(root, textvariable=result).pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
