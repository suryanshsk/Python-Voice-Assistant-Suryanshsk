from imdb import IMDb

class IMDBAPI:
    def __init__(self, api_key):
        self.ia = IMDb(api_key)

    def search_movie(self, movie_title):
        """Search for movies by title"""
        results = self.ia.search_movie(movie_title)
        return results

    def get_movie_details(self, movie_id):
        """Get movie details by ID"""
        movie = self.ia.get_movie(movie_id)
        return movie

    def get_top_250_movies(self):
        """Get top 250 movies"""
        top_250 = self.ia.get_top250_movies()
        return top_250

    def get_movie_cast(self, movie_id):
        """Get movie cast by ID"""
        movie = self.ia.get_movie(movie_id)
        cast = movie['cast']
        return cast

    def get_movie_reviews(self, movie_id):
        """Get movie reviews by ID"""
        movie = self.ia.get_movie(movie_id)
        reviews = movie['reviews']
        return reviews

    def get_person_details(self, person_id):
        """Get person details by ID"""
        person = self.ia.get_person(person_id)
        return person

    def get_person_filmography(self, person_id):
        """Get person filmography by ID"""
        person = self.ia.get_person(person_id)
        filmography = person['filmography']
        return filmography

if __name__ == '__main__':
    api_key = 'your_api_key'  # Replace with your IMDB API key
    imdb = IMDBAPI(api_key)

    # Search movie
    movie_title = 'The Matrix'
    results = imdb.search_movie(movie_title)
    print("Search Results:")
    for result in results:
        print(result['title'], result.movieID)

    # Get movie details
    movie_id = 'tt0133093'  # The Matrix (1999)
    movie = imdb.get_movie_details(movie_id)
    print("\nMovie Details:")
    print(movie['title'], movie['rating'], movie['genre'])

    # Get top 250 movies
    top_250 = imdb.get_top_250_movies()
    print("\nTop 250 Movies:")
    for movie in top_250:
        print(movie['title'], movie['rating'])

    # Get movie cast
    cast = imdb.get_movie_cast(movie_id)
    print("\nMovie Cast:")
    for person in cast:
        print(person['name'], person.currentRole)

    # Get movie reviews
    reviews = imdb.get_movie_reviews(movie_id)
    print("\nMovie Reviews:")
    for review in reviews:
        print(review['header'], review['text'])

    # Get person details
    person_id = 'nm0000129'  # Keanu Reeves
    person = imdb.get_person_details(person_id)
    print("\nPerson Details:")
    print(person['name'], person['birth date'])

    # Get person filmography
    filmography = imdb.get_person_filmography(person_id)
    print("\nPerson Filmography:")
    for role in filmography:
        print(role['title'], role['year'])
