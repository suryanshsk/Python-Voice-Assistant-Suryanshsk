import requests
import json
import os
from colorama import init, Fore, Back, Style

init(autoreset=True)

DATA_FILE = 'profile.json'  # Used to store user profiles

def load_profile():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}  

def save_profile(profiles):
    with open(DATA_FILE, 'w') as file:
        json.dump(profiles, file)

def book_recommendation(preferred_genre):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{preferred_genre}&maxResults=5"
    response = requests.get(api_url)

    if response.status_code == 200:
        books = response.json().get('items', [])
        recommendation = []

        for book in books:
            title = book['volumeInfo'].get('title', 'No title available')
            authors = book['volumeInfo'].get('authors', ['unknown author'])
            cover_image = book['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'no image available')
            recommendation.append({
                'title': title,
                'authors': authors,
                'cover_image': cover_image
            })

        return recommendation
    else:
        print(Fore.RED + "Error in fetching the data")
        return []

def display_recommendation(books):
    if not books:
        print(Fore.YELLOW + "No recommendations found.")
        return

    print(Fore.CYAN + "\nBook Recommendations: ")
    for i, book in enumerate(books, start=1):
        print(Fore.GREEN + f"{i}. Title: {book['title']}")
        print(Fore.MAGENTA + f"  Authors: {', '.join(book['authors'])}")
        print(Fore.LIGHTYELLOW_EX + f"    Cover Image: {book['cover_image']}\n")

def add_to_reading_list(book, user_data):
    user_data['reading_list'].append(book)
    save_profile(user_profiles)
    print(Fore.GREEN + f"{book['title']} has been added to your reading list.")

def rate_review_book(title, user_data):
    rating = input(Fore.YELLOW + "Enter your rating (1-5): ")
    review = input(Fore.YELLOW + "Enter your review: ")
    user_data['reviews'][title] = {'rating': rating, 'review': review}
    save_profile(user_profiles)
    print(Fore.GREEN + f"Thank you for your review of {title}")

def view_reading_list(user_data):
    if not user_data['reading_list']:
        print(Fore.YELLOW + "Your reading list is empty.")
        return

    print(Fore.CYAN + "\nYour Reading List: ")
    for i, book in enumerate(user_data['reading_list'], start=1):
        print(Fore.GREEN + f"{i}. Title: {book['title']}")
        print(Fore.MAGENTA + f"  Authors: {', '.join(book['authors'])}")

def view_reviews(user_data):
    if not user_data['reviews']:
        print(Fore.YELLOW + "You have no reviews yet.")
        return

    print(Fore.CYAN + "\nYour Reviews: ")
    for title, review_data in user_data['reviews'].items():
        print(Fore.LIGHTYELLOW_EX + f"- {title}: {review_data['rating']} stars, Review: {review_data['review']}")

def register_user(username):
    if username in user_profiles:
        print(Fore.RED + "Username already exists. Please choose a different username.")
        return None

    user_profiles[username] = {
        'preferred_genre': '',
        'reading_list': [],
        'reviews': {}
    }
    save_profile(user_profiles)
    print(Fore.GREEN + f"User {username} registered successfully!")
    return user_profiles[username]

def login_user(username):
    if username in user_profiles:
        print(Fore.GREEN + f"Welcome back, {username}!")
        return user_profiles[username]
    else:
        print(Fore.RED + "Username does not exist, please register yourself.")
        return None

def suggested_reading():
    print(Style.BRIGHT + Fore.CYAN + "\nSuggested Readings: ")
    suggested_books = [
        {
            'title': 'The Alchemist',
            'author': 'Paulo Coelho',
            'fact': 'A novel that emphasizes the importance of pursuing one’s dreams.',
            'intro': 'Follow Santiago, a shepherd boy, as he journeys to discover his personal legend.'
        },
        {
            'title': 'Becoming',
            'author': 'Michelle Obama',
            'fact': 'A memoir from the former First Lady of the United States.',
            'intro': 'In this deeply personal memoir, Michelle Obama invites readers into her world.'
        },
        {
            'title': 'Educated',
            'author': 'Tara Westover',
            'fact': 'A memoir that recounts the author’s quest for knowledge.',
            'intro': 'Born to survivalists in the mountains of Idaho, Tara Westover didn’t set foot in a classroom until she was 17.'
        },
        {
            'title': 'The Night Circus',
            'author': 'Erin Morgenstern',
            'fact': 'A fantasy novel set in a magical circus that only opens at night.',
            'intro': 'Two young illusionists, bound by a rivalry, participate in a magical competition that shapes their fates.'
        },
        {
            'title': 'Sapiens: A Brief History of Humankind',
            'author': 'Yuval Noah Harari',
            'fact': 'A non-fiction book that explores the history of humanity.',
            'intro': 'Harari takes readers on a journey through the history of humankind, from the Stone Age to the modern world.'
        }
    ]

    for book in suggested_books:
        print(Fore.GREEN + f"Title: {book['title']}")
        print(Fore.MAGENTA + f"Author: {book['author']}")
        print(Fore.LIGHTYELLOW_EX + f"Fact: {book['fact']}")
        print(Fore.LIGHTWHITE_EX + f"Intro: {book['intro']}\n")

def bestselling_books():
    print(Style.BRIGHT + Fore.CYAN + "\nBestselling Books: ")
    books = [
        {
            'title': 'Where the Crawdads Sing',
            'author': 'Delia Owens',
            'fact': 'This novel spent over 100 weeks on the New York Times bestseller list.',
        },
        {
            'title': 'The Midnight Library',
            'author': 'Matt Haig',
            'fact': 'A thought-provoking story about the choices we make in life.',
        },
        {
            'title': 'The Vanishing Half',
            'author': 'Brit Bennett',
            'fact': 'A multi-generational narrative that tackles themes of race and identity.',
        },
        {
            'title': 'The Book Thief',
            'author': 'Markus Zusak',
            'fact': 'A historical novel narrated by Death, set in Nazi Germany during WWII.',
        },
        {
            'title': 'A Thousand Splendid Suns',
            'author': 'Khaled Hosseini',
            'fact': 'A powerful tale of female friendship, love, and endurance in war-torn Afghanistan.',
        }
    ]

    for book in books:
        print(Fore.GREEN + f"Title: {book['title']}")
        print(Fore.MAGENTA + f"Author: {book['author']}")
        print(Fore.LIGHTYELLOW_EX + f"Fact: {book['fact']}\n")

def main():
    global user_profiles
    user_profiles = load_profile()  # Load profile data

    print(Fore.CYAN + "Welcome to the Book Recommendation Assistant!")

    while True: 
        action = input(Fore.YELLOW + "Do you want to (r)egister, (l)ogin, or (e)xit? ").lower()

        if action == 'e':
            print(Fore.CYAN + "Goodbye!")
            break

        elif action == 'r':
            username = input(Fore.YELLOW + "Enter a username to register: ")
            user_data = register_user(username)
            if user_data is None:
                continue

        elif action == 'l':
            username = input(Fore.YELLOW + "Enter a username to login: ")
            user_data = login_user(username)
            if user_data is None:
                continue

        if user_data:
            preferred_genre = input(Fore.CYAN + "Enter your preferred genre: ")
            user_data['preferred_genre'] = preferred_genre
            save_profile(user_profiles)  

            # Automatically fetch and display book recommendations right after user enters genre
            print(Fore.CYAN + f"\nFetching book recommendations for the genre '{preferred_genre}'...")
            books = book_recommendation(preferred_genre) 
            display_recommendation(books)  

            while True: 
                choice = input(Fore.YELLOW + "Would you like to (a)dd a book to your reading list, (r)ate a book, (v)iew your reading list, (vr) view your reviews, (sr) for suggested readings, (bb) for bestselling books, (br) for book recommendations, or (logout) to switch users? ").lower()

                if choice == 'logout':
                    break

                elif choice == 'br':  # Re-fetch book recommendations upon request
                    books = book_recommendation(preferred_genre)  
                    display_recommendation(books)

                elif choice == 'a':
                    book_choice = int(input(Fore.YELLOW + "Enter the number of the book you want to add to your reading list: ")) - 1
                    add_to_reading_list(books[book_choice], user_data)

                elif choice == 'r':
                    book_choice = int(input(Fore.YELLOW + "Enter the number of the book you want to rate: ")) - 1
                    rate_review_book(books[book_choice]['title'], user_data)

                elif choice == 'v':
                    view_reading_list(user_data)

                elif choice == 'vr':
                    view_reviews(user_data)

                elif choice == 'sr':
                    suggested_reading()

                elif choice == 'bb':
                    bestselling_books()


if __name__ == "__main__":
    main()
