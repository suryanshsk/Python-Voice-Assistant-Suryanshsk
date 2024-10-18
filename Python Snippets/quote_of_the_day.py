import requests
import pickle
import os

FAVOURITES = "favourite_quotes.pkl"
favourite_quotes = []

def load_favourites():
    global favourite_quotes
    if os.path.exists(FAVOURITES):
        with open(FAVOURITES, "rb") as file:
            favourite_quotes = pickle.load(file)
        print("Loaded your favourite quotes.")
    else:
        print("No favourite quotes to load.")

def save_favourites_to_file():
    with open(FAVOURITES, "wb") as file:
        pickle.dump(favourite_quotes, file)

def show_favourites():
    if favourite_quotes:
        print("Your favourite quotes:")
        for idx, quote in enumerate(favourite_quotes, 1):
            print(f"{idx}. {quote}")
    else:
        print("No favourite quotes saved yet!")

def save_favourite(quote):
    favourite_quotes.append(quote)
    print("The quote has been saved to favourites!")
    save_favourites_to_file()

def clear_favourites():
    if favourite_quotes:
        favourite_quotes.clear()
        print("All favourite quotes have been cleared.")
    else:
        print("No favourite quotes to clear.")

def delete_favourite():
    show_favourites()
    if favourite_quotes:
        try:
            choice = int(input("Enter the number of the quote you want to delete: ")) - 1
            if 0 <= choice < len(favourite_quotes):
                removed_quote = favourite_quotes.pop(choice)
                print(f"Deleted quote: {removed_quote}")
                save_favourites_to_file()
            else:
                print("Invalid choice, no quote deleted.")
        except ValueError:
            print("Please enter a valid number.")

def get_quote_of_the_day():
    try:
        response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
        response.raise_for_status()  # Check for HTTP errors
        quote_data = response.json()
        quote = f"{quote_data['quoteText']} — {quote_data['quoteAuthor']}"
        print(f"\nQuote of the Day: {quote}")
        return quote
    except requests.RequestException as e:
        print(f"Error fetching quote: {e}")
        return None

def quote_voice_assistant():
    load_favourites()
    while True:
        print("\nWhat would you like to do?")
        print("1. Get a Quote of the Day")
        print("2. Save the current quote to favourites")
        print("3. Show favourite quotes")
        print("4. Clear all favourite quotes")
        print("5. Delete a favourite quote")
        print("6. Exit")

        choice = input("Please select an option (1-6): ")

        if choice == "1":
            current_quote = get_quote_of_the_day()
        elif choice == "2":
            if 'current_quote' in locals() and current_quote is not None:
                save_favourite(current_quote)
            else:
                print("No quote has been displayed yet.")
        elif choice == "3":
            show_favourites()
        elif choice == "4":
            clear_favourites()
        elif choice == "5":
            delete_favourite()
        elif choice == "6":
            print("Bye, take care!")
            break
        else:
            print("Oops! That's not on the list, try again.")

if __name__ == "__main__":
    quote_voice_assistant()
