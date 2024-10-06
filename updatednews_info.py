import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_news(api_key, category=None, country='us', num_articles=5):
    """
    Fetches the latest news headlines from the News API.

    Args:
        api_key (str): Your News API key.
        category (str): Optional news category (e.g., business, technology).
        country (str): Country code for news (default is 'us').
        num_articles (int): Number of articles to retrieve (default is 5).

    Returns:
        list: A list of news article titles.
    """
    url = f'https://newsapi.org/v2/top-headlines?apiKey={api_key}&country={country}'
    
    if category:
        url += f"&category={category}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses (4xx and 5xx)

        data = response.json()
        articles = data.get('articles', [])

        # Handle case where no articles are returned
        if not articles:
            print("No articles found.")
            return []

        # Return the specified number of articles
        return [article['title'] for article in articles[:num_articles]]

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except KeyError as key_err:
        print(f"Key error: {key_err}")
    
    return []

# Example usage:
if __name__ == '__main__':
    api_key = os.environ.get('NEWS_API_KEY')
    headlines = get_news(api_key, category='technology')
    for title in headlines:
        print(title)
