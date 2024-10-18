import pyjokes
import pickle
import os

favourites = []
last_joke = ""

FAVOURITES = "favourites.pkl"

def load_favourites():
    global favourites
    if os.path.exists(FAVOURITES):
        with open(FAVOURITES, "rb") as file:
            favourites = pickle.load(file)
        print("Load the favourite jokes from previous visit")
        show_favourites()
    else:
        print("No favourites jokes to load")

def save_favourites_to_file():
    with open(FAVOURITES, "wb") as file:
        pickle.dump(favourites, file)

def clear_loaded_favourites():
    global favourites
    if os.path.exists(FAVOURITES):
        os.remove(FAVOURITES)
        favourites = []
        print("Loaded jokes from previous visit cleared")
    else:
        print("No loaded jokes to clear")

def tell_joke(category='neutral'):
    global last_joke
    try:
        joke = pyjokes.get_joke(category=category)
        last_joke = joke
        print(joke)
    except ValueError as error:
        print(f"Error in fetching joke: {error}")
        print("Falling back to a neutral joke")
        last_joke = pyjokes.get_joke(category='neutral')
        print(last_joke)

def get_category_jokes():
    print("Choose a joke category:")
    print("1. Neutral")
    print("2. Chuck Norris")
    print("3. Twister")
    print("4. All")
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        return "neutral"
    elif choice == "2" or choice == "3":
        return "all"
    elif choice == "4":
        return "all"
    else:
        print("Oops! That's not on the list. Let's go to neutral for now!")
        return "neutral"


def show_favourites():
    if favourites:
        print("Your favourite jokes:")
        for idx, joke in enumerate(favourites, 1):
            print(f"{idx}. {joke}")
    else:
        print("No favorite jokes saved yet!")

def save_favourites(joke):
    favourites.append(joke)
    print("The joke saved to favourites!!")
    save_favourites_to_file()

def clear_favourites():
    if favourites:
        favourites.clear()
        print("All favourites jokes are cleared")
    else:
        print("No favourites jokes to clear")

def delete_favourite():
    show_favourites()
    if favourites:
        try:
            choice = int(input("Enter the number of the joke you want to delete: ")) - 1
            if 0 <= choice < len(favourites):
                removed_joke = favourites.pop(choice)
                print(f"Deleted joke: {removed_joke}")
                save_favourites_to_file()
            else:
                print("Invalid choice, no joke deleted.")
        except ValueError:
            print("Please enter a valid number.")

def joke_voice_assistant():
    load_favourites()
    while True:
        print("\nWhat would you like to do?")
        print("1. Tell me a new joke")
        print("2. Repeat the previous joke")
        print("3. Save the last joke to favourites")
        print("4. Show favourite ones!")
        print("5. Clear all the favourite jokes")
        print("6. Delete a favourite jokes")
        print("7. Show the favourite joke from previous visit")
        print("8. Clear loaded jokes from previous visit")
        print("9. Exit")

        choice = input("Please select option (1-9): ")

        if choice == "1":
            category = get_category_jokes()
            tell_joke(category)
        elif choice == "2":
            if last_joke:
                print(f"Last joke: {last_joke}")
            else:
                print("No joke has been told.")
        elif choice == "3":
            if last_joke:
                save_favourites(last_joke)
            else:
                print("No joke has been told.")
        elif choice == "4":
            show_favourites()
        elif choice == "5":
            clear_favourites()
        elif choice == "6":
            delete_favourite()
        elif choice == "7":
            load_favourites()
        elif choice == "8":
            clear_loaded_favourites()
        elif choice == "9":
            print("Bye, take care!!")
            break
        else:
            print("Oops! That's not on the list, try again later")

if __name__ == "__main__":
    joke_voice_assistant()