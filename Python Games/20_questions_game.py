import random
import time

class TwentyQuestionsGame:
    
    def __init__(self):
        self.knowledge_base = {
            
            "animal": ["dog", "cat", "elephant", "lion", "tiger", "rabbit"],
            "bird": ["sparrow", "eagle", "parrot", "penguin", "owl", "flamingo", "hummingbird", "falcon"],
            "plant": ["tree", "flower", "grass", "cactus"],
            "technology": ["smartphone", "computer", "drone", "robot", "camera"],
            "vehicles": ["car", "motorcycle", "airplane", "boat", "bicycle"],
            "food": ["pizza", "sushi", "burger", "pasta", "cake"],
            "tools": ["hammer", "screwdriver", "drill", "wrench"],
            "household": ["sofa", "bed", "table", "chair", "lamp"],
            "country": ["India", "France", "Brazil", "USA", "China", "Pakistan", "Iran", "Iraq"],
            "musical instruments": ["guitar", "piano", "drums", "violin", "saxophone", "flute", "trumpet", "harp"],
            "movies": ["Inception", "The Matrix", "Titanic", "Avatar", "Gladiator", "The Godfather", "Pulp Fiction", "Jurassic Park"],
            "sports": ["soccer", "basketball", "tennis", "cricket", "baseball", "hockey", "golf", "swimming"],
            "mythical creatures": ["dragon", "unicorn", "phoenix", "mermaid", "griffin", "centaur", "golem", "werewolf"],
            "colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white"],
            "emotions": ["happiness", "sadness", "anger", "fear", "surprise", "disgust", "love", "anxiety"],
        }
        
        self.categories = list(self.knowledge_base.keys())
        self.score = 0
        self.guess_limit = 20
        self.difficulty_levels = {
            "easy": {"guess_limit": 20, "hint": True},
            "medium": {"guess_limit": 15, "hint": False},
            "hard": {"guess_limit": 10, "hint": False}
        }
        
        self.current_difficulty = "easy"
        self.hint_used = False
        self.achievements = []

    def ask_yes_no(self, question):
        answer = input(f"{question} (yes/no): ").strip().lower()
        while answer not in ["yes", "no"]:
            answer = input("Please answer with 'yes' or 'no' only: ").strip().lower()
        return answer == "yes"

    def guess_object(self, category, guessed_objects):
        remaining_objects = [obj for obj in self.knowledge_base[category] if obj not in guessed_objects]
        if remaining_objects:
            guess = random.choice(remaining_objects)
            guessed_objects.append(guess)
            return guess
        return None

    def learn_new_object(self, category):
        new_object = input("What was your object? ").strip().lower()
        self.knowledge_base[category].append(new_object)
        print(f"{new_object} has been added to my brain under the {category} category! 🧠")

    def provide_hint(self, category):
        if self.hint_used:
            print("Oops! You've already used your hint. Can't help you twice, my friend! 😉")
            return

        if len(self.knowledge_base[category]) > 0:
            hint = random.choice(self.knowledge_base[category])
            print(f"Hint: It could be something like... {hint}.")
            self.hint_used = True
        else:
            print("Hmm, no hints for this category. My brain's feeling a bit empty here! 😅")

    def select_difficulty(self):
        while True:
            level = input("Choose your challenge level (easy/medium/hard): ").strip().lower()
            if level in self.difficulty_levels:
                self.current_difficulty = level
                self.guess_limit = self.difficulty_levels[level]["guess_limit"]
                print(f"You're feeling brave, huh? {level.capitalize()} mode it is!")
                break
            else:
                print("Invalid level. Try again, warrior of guesses!")

    def play_game(self):
        print("🎉 Welcome to the Ultimate 20 Questions Showdown! 🎉")
        self.select_difficulty()

        while True:
            print(f"Categories: {', '.join(self.categories)}")
            category = input("Pick a category to challenge me: ").strip().lower()

            if category not in self.categories:
                print("Oops! That's not a valid category. Give it another shot!")
                continue

            if self.ask_yes_no(f"Do you want a hint to spice things up? (Only in {self.current_difficulty} mode)") and self.difficulty_levels[self.current_difficulty]["hint"]:
                self.provide_hint(category)

            remaining_guesses = self.guess_limit
            guessed_objects = []
            print(f"Let the guessing begin! You have {remaining_guesses} guesses left.")

            while remaining_guesses > 0:
                guess = self.guess_object(category, guessed_objects)
                if guess:
                    print(f"🧐 Is it... a {guess}?")
                    if self.ask_yes_no("Am I right?"):
                        print(f"🎉 Woohoo! I guessed your object: {guess}! Score one for me! 🎉")
                        self.score += 1
                        if remaining_guesses == self.guess_limit:
                            print("Achievement Unlocked: Mind Reader! 🧠")
                            self.achievements.append("Mind Reader")
                        break
                    else:
                        print(f"Oh no! I was {random.randint(50, 100)}% sure I had it!")
                        playful_response = random.choice([
                            "But hey, nobody's perfect. 😅",
                            "Give me a break, I'm still learning! 😜",
                            "Hmm, tough one. Let's try again!"
                        ])
                        print(playful_response)
                else:
                    print("I'm out of ideas! 🫠")
                    break

                remaining_guesses -= 1
                print(f"{remaining_guesses} guesses remaining...")

            if remaining_guesses == 0:
                print("😔 Oh no, I've run out of guesses.")
                if self.ask_yes_no("Want to teach me your secret object?"):
                    self.learn_new_object(category)

            print(f"Your current score: {self.score}. Achievements: {', '.join(self.achievements) if self.achievements else 'None yet!'}")
            if not self.ask_yes_no("Would you like to play another round?"):
                print("Thanks for playing! You're the real winner here. See you next time! 👋")
                break

if __name__ == "__main__":
    game = TwentyQuestionsGame()
    game.play_game()
