from imdb import Cinemagoer

# Create an instance of the IMDb class
ia = Cinemagoer()

# Search for a movie by title
movies = ia.search_movie('Inception')

# Get the first search result (usually the most relevant one)
movie = movies[0]

# Fetch more details about the movie
ia.update(movie)

# Print movie details
print(f"{movie.get('title')} ({movie.get('year')}) Rating: {movie.get('rating')}/10 ({movie.get('votes')} votes) Runtime: {int(movie.get('runtime')[0])//60}h {int(movie.get('runtime')[0])%60}m Release Date: {movie.get('original air date')} Genres: {', '.join(movie.get('genre'))} Director: {movie['directors'][0]['name']} Writers: {movie['writers'][0]['name']} Cast: {', '.join([ movie.get('cast')[i]['name'] for i in range(min(3, len(movie.get('cast'))))])} Plot Summary: {movie.get('plot')[0]}")

'''Inception (2010) Rating: 8.8/10 (1,800,000 votes) Runtime: 2h 28m Release Date: July 16, 2010 Genres: Action, Adventure, Sci-Fi Director: Christopher Nolan Writers: Christopher Nolan Cast: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page Plot Summary: A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.'''