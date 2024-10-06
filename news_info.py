import requests
import json
import os

def get_news(api_key, category='general', page=1, page_size=5, query=None):
    try:
        base_url = 'https://newsapi.org/v2/top-headlines' if not query else 'https://newsapi.org/v2/everything'
        params = {
            'apiKey': api_key,
            'category': category,
            'page': page,
            'pagesize': page_size
        }

        if query:
            params.pop('category')
            params['q'] = query

        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()
        articles = data.get('articles', [])

        return articles

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return []

def save_articles(articles, filename='articles.json'):
    with open(filename, 'w') as f:
        json.dump(articles, f, indent=4)
    print(f"Articles saved to {filename}.")

def main():
    API_KEY = os.environ.get('NEWS_API_KEY')
    if not API_KEY:
        print("Please set the NEWS_API_KEY environment variable.")
        return

    category = input("Enter news category (such as: general, business, technology, sports, entertainment, politics, health and science): ")
    while True:
        try:
            num_articles = int(input("How many articles would you like to see? "))
            if num_articles <= 0:
                print("Please enter a positive integer.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    query = input("Enter a keyword to search for articles (or press Enter to skip): ")
    if query == "":
        query = None

    articles = get_news(API_KEY, category=category, page_size=num_articles, query=query)

    if articles:
        save_articles(articles)
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Author: {article.get('author', 'N/A')}")
            print(f"Published at: {article['publishedAt']}")
            print(f"Description: {article.get('description', 'N/A')}\n")

if __name__ == "__main__":
    main()
    