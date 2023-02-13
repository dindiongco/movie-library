import os

SEARCH_MOVIE_URL = 'https://api.themoviedb.org/3/search/movie'
ID_URL = 'https://api.themoviedb.org/3/movie'
TOP_RATED_MOVIE = 'https://api.themoviedb.org/3/movie/popular'
API_KEY = os.environ.get('TMDB_KEY')
APP_HEADERS = {
    'api_key': API_KEY
}
