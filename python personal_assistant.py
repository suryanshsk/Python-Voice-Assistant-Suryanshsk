import wikipediaapi
import datetime
import requests
import pyttsx3
import spacy

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia('en')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Greet the user
def greet_user():
    greeting = "Hello! I am your Python assistant. How can I help you today?"
    print(greeting)
    speak(greeting)

# Get current time
def get_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    response = f"The current time is {time_str}."
    print(response)
    speak(response)

# Fetch summary from Wikipedia
def search_wikipedia(query):
    page = wiki_wiki.page(query)
    if page.exists():
        summary = page.summary[:300]  # Get the first 300 characters of the summary
        print(f"According to Wikipedia: {summary}")
        speak(f"According to Wikipedia, {summary}")
    else:
        print("Sorry, I couldn't find that information on Wikipedia.")
        speak("Sorry, I couldn't find that information on Wikipedia.")

# Get stock price (requires Alpha Vantage API key)
def get_stock_price(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (1min)" in data:
        latest_time = next(iter(data["Time Series (1min)"]))
        latest_data = data["Time Series (1min)"][latest_time]
        price = latest_data["1. open"]
        stock_info = f"The current stock price of {symbol} is ${price}."
        print(stock_info)
        speak(stock_info)
    else:
        print("Sorry, I couldn't retrieve the stock information.")
        speak("Sorry, I couldn't retrieve the stock information.")

# Get latest news (requires News API key)
def get_latest_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "ok":
        articles = data["articles"][:5]  # Get the top 5 articles
        news_list = "\n".join([f"- {article['title']}" for article in articles])
        news_report = f"Here are the top news headlines:\n{news_list}"
        print(news_report)
        speak(news_report)
    else:
        print("Sorry, I couldn't fetch the news.")
        speak("Sorry, I couldn't fetch the news.")

# Handle user input with NLP
def handle_command(command):
    doc = nlp(command)
    
    if "time" in command:
        get_time()
    elif "wikipedia" in command or any(token.lemma_ == "know" for token in doc):
        query = input("What do you want to know about? ")
        search_wikipedia(query)
    elif "stock" in command:
        symbol = input("Enter the stock symbol: ")
        api_key = "your_alpha_vantage_api_key"  # Replace with your Alpha Vantage API key
        get_stock_price(symbol, api_key)
    elif "news" in command:
        api_key = "your_news_api_key"  # Replace with your News API key
        get_latest_news(api_key)
    elif "exit" in command:
        print("Goodbye!")
        speak("Goodbye!")
        return True
    else:
        print("I'm sorry, I didn't understand that command.")
        speak("I'm sorry, I didn't understand that command.")
    return False

# Main function
def main():
    greet_user()
    while True:
        user_input = input("Enter a command (or type 'exit' to quit): ").lower()
        if handle_command(user_input):
            break

# Run the assistant
if __name__ == "__main__":
    main()
