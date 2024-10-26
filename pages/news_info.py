import requests
import json
import os
import streamlit as st

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
        st.error(f"An error occurred: {e}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON: {e}")
        return []

def save_articles(articles, filename='articles.json'):
    with open(filename, 'w') as f:
        json.dump(articles, f, indent=4)
    st.success(f"Articles saved to {filename}.")

def main():
    st.title("News Fetcher")

    API_KEY = os.environ.get('NEWS_API_KEY')
    if not API_KEY:
        st.error("Please set the NEWS_API_KEY environment variable.")
        return

    category = st.selectbox("Enter news category", ['general', 'business', 'technology', 'sports', 'entertainment', 'politics', 'health', 'science'])
    num_articles = st.number_input("How many articles would you like to see?", min_value=1, step=1)
    query = st.text_input("Enter a keyword to search for articles (or leave blank to skip)")

    if st.button("Fetch News"):
        articles = get_news(API_KEY, category=category, page_size=num_articles, query=query if query else None)

        if articles:
            save_articles(articles)
            for article in articles:
                st.subheader(article['title'])
                st.write(f"**Author:** {article.get('author', 'N/A')}")
                st.write(f"**Published at:** {article['publishedAt']}")
                st.write(f"**Description:** {article.get('description', 'N/A')}\n")

if __name__ == "__main__":
    main()
