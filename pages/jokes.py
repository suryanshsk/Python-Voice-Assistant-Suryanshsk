import requests
from textblob import TextBlob
import streamlit as st

def get_random_joke():
    joke_url = "https://icanhazdadjoke.com/"
    emoji_map = {
        "positive": "😊",
        "neutral": "😐",
        "negative": "😢"
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    def get_sentiment(joke):
        analysis = TextBlob(joke)
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"

    try:
        joke_response = requests.get(joke_url, headers=headers)
        joke_response.raise_for_status()
        joke_data = joke_response.json()
        joke = joke_data["joke"]

        sentiment = get_sentiment(joke)
        emoji = emoji_map.get(sentiment, "")

        return f"{joke} {emoji}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching joke: {e}"

# Streamlit app
st.title("Random Joke Generator")

if st.button("Get a Random Joke"):
    joke = get_random_joke()
    st.write(joke)