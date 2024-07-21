import requests

def get_news():
    # Example API call, replace with a real news API
    api_key = 'YOUR_API_KEY'
    response = requests.get(f'https://newsapi.org/v2/top-headlines?apiKey={api_key}')
    data = response.json()
    for article in data['articles'][:5]:
        print(article['title'])
