import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def ensure_vader_lexicon():
    """
    Ensures that the VADER lexicon is downloaded. Downloads it if not already available.
    """
    try:
        # Check if VADER lexicon is available
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        # Download the VADER lexicon if not found
        nltk.download('vader_lexicon')

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text using VADER sentiment analysis.

    Args:
        text (str): The text to analyze sentiment for.

    Returns:
        dict: A dictionary containing the sentiment scores for the text.
    """
    ensure_vader_lexicon()  # Ensure VADER lexicon is available
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    return sentiment_scores

# Example usage
if __name__ == "__main__":
    sample_text = "I absolutely love this product! It's amazing."
    sentiment_result = analyze_sentiment(sample_text)
    print("Sentiment Analysis Result:", sentiment_result)
