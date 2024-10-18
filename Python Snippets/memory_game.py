import random
import time
import json

FRUITS = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi", "lemon", "mango", "orange", "papaya"]
CLOTHES = ["shirt", "pants", "dress", "jacket", "skirt", "hat", "scarf", "gloves", "shoes", "socks"]
ANIMALS = ["dog", "cat", "elephant", "tiger", "lion", "giraffe", "zebra", "bear", "rabbit", "fox"]
COLORS = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white", "grey"]
VEHICLES = ["car", "bus", "bicycle", "motorcycle", "airplane", "train", "boat", "truck", "scooter", "van"]
FOOD = ["pizza", "burger", "sushi", "pasta", "salad", "taco", "sandwich", "ice cream", "cake", "cookies"]
COUNTRIES = ["USA", "India", "China", "Brazil", "Germany", "Australia", "Canada", "Japan", "France", "Italy", "Korea", "Norway"]

def generate_sequence(length):
    words = FRUITS + CLOTHES + ANIMALS + COLORS + VEHICLES + FOOD + COUNTRIES
    return random.sample(words, length)

def save_game_data(username, score, high_score):
    username = username.lower()  
    data = {}
    try:
        with open("leaderboard.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

    data[username] = {'score': score, 'high_score': max(score, data.get(username, {}).get('high_score', 0))}
    with open("leaderboard.json", "w") as file:
        json.dump(data, file)

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def display_leaderboard():
    leaderboard = load_leaderboard()
    if leaderboard:
        print("\nLeaderboard:")
        for user, scores in leaderboard.items():
            print(f"{user.capitalize()}: High Score - {scores['high_score']}")
    else:
        print("\nNo scores available yet.")

def play_memory_game():
    print("Welcome to the Memory Game!")
    print("You will see a sequence of random words, let's see how much you can remember!!")

    username = input("Enter your username: ").strip()
    high_score = 0

    while True:
        score = 0
        level = 1

        while True:
            game_mode = input("Choose a game mode (classic/timed/practice): ").strip().lower()
            if game_mode in ["classic", "timed", "practice"]:
                break
            else:
                print("Invalid choice! Please choose either 'classic', 'timed', or 'practice'.")

        timed = game_mode == "timed"
        
        while True: 
            sequence = generate_sequence(level)
            print(f"\nLevel: {level}")
            print("Remember this sequence: ")
            print(" ".join(sequence))
            
            time.sleep(3)
            print("\n" + "\n" * 20)  # Added more line breaks
            time.sleep(1)
            
            response_time = 20 if timed else 30
            print(f"You have {response_time} seconds to repeat the sequence.")
            start_time = time.time()
            user_input = input("Repeat the sequence (separate words with space): ").strip().lower().split()
            
            elapsed_time = time.time() - start_time
            
            if elapsed_time > response_time:
                print("Time's up! You took too long to respond, better luck next time.")
                break
            
            if user_input == sequence:
                print("\033[92mCorrect! Moving to the next level.\033[0m")
                score += 1
                level += 1
                if score > high_score:
                    high_score = score
                    print("New High Score!")
                
                print(f"Your current score: {score}")
                print(f"High score: {high_score}")

                save_game_data(username, score, high_score)

            else:
                print(f"\033[91mIncorrect! The correct sequence was: {' '.join(sequence)}\033[0m")
                break
            
        print(f"Your final score: {score}")
        print(f"High score: {high_score}")
        
        display_leaderboard()
        
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            return

if __name__ == "__main__":
    play_memory_game()
