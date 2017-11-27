from flask import Blueprint


# Create blueprint for movies module
mod_movies = Blueprint('movies', __name__)

from imdb_rest.movies.movies import *
