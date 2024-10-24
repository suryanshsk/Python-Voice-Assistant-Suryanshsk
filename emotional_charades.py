import random
import time
from inputimeout import inputimeout, TimeoutOccurred
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

clues = {
    
    "ecstatic": "Pretend you're feeling very happy.",
    "scared": "Act out being frightened.",
    "surprised": "Show what it feels like to be shocked.",
    "frustrated": "Demonstrate being annoyed or upset.",
    "sad": "Express feelings of unhappiness.",
    "calm": "Illustrate being peaceful and relaxed.",
    "angry": "Act out being mad.",
    "confused": "Show what it feels like when you're unsure.",
    "excited": "Demonstrate enthusiasm and eagerness.",
    "bored": "Act like you have nothing to do."
}

score = 0
total_guesses = 0
correct_guesses = 0
time_limit = 10

# Difficulty level selection
def get_difficulty():
    while True:
        try:
            level = int(input(Fore.CYAN + "Choose difficulty level (1: Easy, 2: Medium, 3: Hard): "))
            if level in [1, 2, 3]:
                return level
            else:
                print(Fore.RED + "Invalid choice! Please choose a level among 1, 2 and 3.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

# Main game logic
def main():
    global score, total_guesses, correct_guesses
    print(Fore.GREEN + "Welcome to Emotional Charades!")

    difficulty_level = get_difficulty()

    print(Fore.CYAN + "You'll be given a clue to act out.")
    print(Fore.CYAN + "Type 'quit' at any time to end the game.")

    while True:
        clue = random.choice(list(clues.keys()))
        print(Fore.MAGENTA + f"\nYour clue is: {clues[clue]}")
        total_guesses += 1

        # Start input timeout
        try:
            user_guess = inputimeout(prompt=Fore.WHITE + "\nEnter your guess (or 'hint' for a hint, 'quit' to exit): ", timeout=time_limit).strip().lower()
        except TimeoutOccurred:
            user_guess = None

        # If user guessed or timed out
        if user_guess == 'quit':
            print(Fore.GREEN + "\nThanks for playing! Goodbye!")
            break
        elif user_guess == 'hint':
            print(Fore.YELLOW + f"Hint: {clues[clue]}")
            continue
        else:
            print(Fore.BLUE + f"Your guess: '{user_guess}' | Correct answer: '{clue}'")
            if user_guess == clue.lower():
                print(Fore.GREEN + "Great job! You guessed it!")
                score += difficulty_level * 2
                correct_guesses += 1
                print(Fore.CYAN + f"Your score: {score}")
            else:
                print(Fore.RED + f"Nice try! The emotion was: {clue}")

    
    print(Fore.GREEN + "\nGame Over!")
    print(Fore.CYAN + f"Total guesses made: {total_guesses}")
    print(Fore.CYAN + f"Total correct guesses: {correct_guesses}")
    print(Fore.CYAN + f"Your final score: {score}")
    
    # Feedback and Suggestions
    feedback_score = (correct_guesses / total_guesses) * 100 if total_guesses > 0 else 0
    print(Fore.YELLOW + f"Your performance: {feedback_score:.2f}% correct guesses.")
    
    if feedback_score == 100:
        print(Fore.GREEN + "Amazing job! You're a charades master!")
    elif feedback_score >= 75:
        print(Fore.GREEN + "Great work! You're doing really well!")
    elif feedback_score >= 50:
        print(Fore.YELLOW + "Good effort! Keep practicing!")
    else:
        print(Fore.RED + "Don't be discouraged! Every guess counts, keep trying!")

if __name__ == "__main__":
    main()
