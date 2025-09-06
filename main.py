from flask import Flask, render_template
from flask import request
import requests
import tmdb_client
from tmdb_client import get_movie_cast, get_movies_list, get_single_movie


app = Flask(__name__)

@app.route('/')
def homepage():
    # Lista dozwolonych typów list
    valid_list_types = ['now_playing', 'popular', 'top_rated', 'upcoming']

    # Pobierz typ listy z parametrów URL
    selected_list = request.args.get('list_type', 'popular')

    # Walidacja: jeśli typ nie jest poprawny, ustaw na 'popular'
    if selected_list not in valid_list_types:
        selected_list = 'popular'

    # Pobierz filmy z TMDB
    movies = tmdb_client.get_movies_list(list_type=selected_list)["results"][:8]

    # Przekaż dane do szablonu
    return render_template(
        "homepage.html",
        movies=movies,
        current_list=selected_list,
        list_types=valid_list_types
    )

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    movie = get_single_movie(movie_id)
    cast = get_movie_cast(movie_id)[:8]
    return render_template("movie_details.html", movie=movie, cast=cast)


if __name__ == '__main__':
    app.run(debug=True)