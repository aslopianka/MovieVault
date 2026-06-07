import json

from utils import color_text

FILENAME = "../movies_data.json"


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.
    The function loads the information from the JSON
    file and returns the data.
    """
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    try:
        with open(FILENAME, "w") as file:
            json.dump(movies, file, indent=4)
    except FileNotFoundError:
        print(color_text("File not found.", "ERROR"))


def add_movie(title, rating, year):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()

    movies[title] = {
        "rating": rating,
        "year": year
    }
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    with open(FILENAME, "r") as file:
        movies = json.load(file)
        movies.pop(title)
        save_movies(movies)


def update_movie(title, rating, year):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    with open(FILENAME, "r") as file:
        movies = json.load(file)
        movies[title]["rating"] = rating
        movies[title]["year"] = year
        save_movies(movies)
