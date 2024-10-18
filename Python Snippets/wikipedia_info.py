import wikipedia
import logging
import time


logging.basicConfig(filename='wikipedia_search.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


search_history = []

def search_wikipedia(query, num_sentences=1, lang='en'):

    wikipedia.set_lang(lang)  
    try:
        
        summary = wikipedia.summary(query, sentences=num_sentences)
        search_history.append({'query': query, 'language': lang, 'summary': summary})
        
        logging.info(f"Successfully searched for '{query}' in language '{lang}' with {num_sentences} sentence(s) on {time.strftime('%Y-%m-%d at %H:%M:%S')}")
        print(f"\n--- Search Result ---\nQuery: {query}\nLanguage: {lang}\nSummary: {summary}\n")
    
    except wikipedia.exceptions.DisambiguationError as e:
        
        logging.warning(f"Disambiguation error for: {query}, options: {e.options}")
        print(f"\nDisambiguationError: Your search term '{query}' is ambiguous. Possible options are:\n")
        for option in e.options:
            print(f"- {option}")
    
    except wikipedia.exceptions.PageError:
        
        logging.error(f"PageError: No page found for: {query}")
        print(f"\nPageError: No page found for '{query}'. Please try again with a different term.\n")
    
    except Exception as e:
    
        logging.error(f"Error: {e}")
        print(f"\nError: {e}\n")


def show_search_history():
   
    if search_history:
        print("\n--- Search History ---\n")
        for index, entry in enumerate(search_history, 1):
            print(f"{index}. Query: {entry['query']} | Language: {entry['language']}\nSummary: {entry['summary']}\n")
    else:
        print("\nNo search history is found.\n")

def main():
    while True:
        print("\nMenu:\n1. Search Wikipedia\n2. View Search History\n3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            query = input("\nEnter the search query: ")
            num_sentences = input("How many sentences do you want in the summary? (default 1): ")
            lang = input("Enter language code (default 'en'): ")
            
            
            num_sentences = int(num_sentences) if num_sentences else 1
            lang = lang if lang else 'en'
            
            
            search_wikipedia(query, num_sentences, lang)
        
        elif choice == '2':

            show_search_history()
        
        elif choice == '3':
            print("\nExiting the program.")
            break
        
        else:
            print("\nInvalid choice.\n")


if __name__ == "__main__":
    main()

