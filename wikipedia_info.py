import wikipedia

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=1)
        print(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        print("DisambiguationError: ", e.options)
    except wikipedia.exceptions.PageError:
        print("PageError: Page not found")
    except Exception as e:
        print(f"Error: {e}")
