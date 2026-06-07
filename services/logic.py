"""Business logic for movie operations."""

import statistics
import random

from matplotlib import pyplot as plt

from api.fetch_movie_data import fetch_movie_data
from utils import color_text
from db import movie_storage_sql as movie_db
from services import html_generator

TEMPLATE_PATH = "templates/index_template.html"
WEBSITE_OUTPUT_PATH = "dist/index.html"


def list_movies():
    """Return all movies formatted as a displayable list."""
    movies = movie_db.list_movies()
    if len(movies) == 0:
        raise ValueError("No movies found.")

    return {
        "type": "list",
        "color_code": "MENU",
        "data": [f"{movie} - rating: {movies[movie]['rating']}, year: {movies[movie]['year']}" for movie in movies]
    }


def add_movie(movie_name):
    """Fetch movie data from the OMDB API and add it to the database."""
    movies = movie_db.list_movies()

    if not movie_name:
        raise ValueError("Please enter all the required information.")

    if movie_name in movies:
        raise ValueError(f"Movie '{movie_name}' already exists.")


    api_response = fetch_movie_data(movie_name)
    if api_response["Response"] == 'True':
        movie_db.add_movie(api_response["Title"], api_response["Year"], api_response["imdbRating"], api_response["Poster"])
    else: raise ValueError(api_response["Error"])

    return {
        "type": "message",
        "color_code": "SUCCESS",
        "data": f"Movie '{movie_name}' added successfully."
    }


def update_movie(movie_to_update, new_rating, new_year):
    """Update a movie's rating in the database."""
    movies = movie_db.list_movies()
    message, color_code = f"Movie '{movie_to_update}' updated successfully.", "SUCCESS"

    if not movies.get(movie_to_update):
        message = f"Movie '{movie_to_update}' not found."
        color_code = "ERROR"

    else:
        new_rating = round(float(new_rating), 1)
        movie_db.update_movie(movie_to_update, new_rating)

    return {
        "type": "message",
        "color_code": color_code,
        "data": message
    }


def delete_movie(movie_name):
    """Delete a movie from the database by title."""
    movies = movie_db.list_movies()

    if movie_name in movies:
        movie_db.delete_movie(movie_name)

    else:
        raise KeyError(f"Movie '{movie_name}' not found.")

    return {
        "type": "message",
        "color_code": "SUCCESS",
        "data": f"Movie '{movie_name}' deleted successfully."
    }


def get_random_movie():
    """Pick and return a random movie from the database."""
    movies = movie_db.list_movies()
    movie = random.choice(list(movies))

    return {
        "type": "message",
        "color_code": "MENU",
        "data": f"{movie} - {movies[movie]['rating']}"
    }


def search_movie(search_term):
    """Search for movies whose title contains the given search term."""
    movies = movie_db.list_movies()
    filtered_movies = []

    for movie in movies:
        if search_term.lower() in movie.lower():
            filtered_movies.append(f"{movie}: {movies[movie]['rating']}")

    if len(filtered_movies) == 0:
        return {
            "type": "message",
            "color_code": "ERROR",
            "data": f"Sorry, movie '{search_term}' not found."
        }

    return {
        "type": "list",
        "color_code": "MENU",
        "data": filtered_movies
    }


def get_movies_sorted_by_rating():
    """Return all movies sorted by rating in descending order."""
    movies = movie_db.list_movies()
    sorted_movies = sorted(
        movies.items(), # returns a list of tuples (movie_name, {movie_info})
        key=lambda item: item[1]["rating"],
        reverse=True
    )

    return {
        "type": "list",
        "color_code": "MENU",
        "data": [f"{movie} - {info['rating']}" for movie, info in sorted_movies]
    }


def get_movies_sorted_chronologically(sorting_direction):
    """Return all movies sorted by year in the given direction ('ASC' or 'DESC')."""
    print(sorting_direction)
    direction = True if sorting_direction.upper() == "DESC" else False

    movies = movie_db.list_movies()
    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]["year"],
        reverse=direction
    )

    return {
        "type": "list",
        "color_code": "MENU",
        "data": [f"{movie} - {info['rating']}, ({info['year']})" for movie, info in sorted_movies]
    }


def get_stats():
    """Calculate and return best, worst, median, and average movie ratings."""
    movies = movie_db.list_movies()
    best_movie_name, best_movie_info = max(movies.items(), key=lambda item: item[1]['rating'])
    worst_movie_name, worst_movie_info = min(movies.items(), key=lambda item: item[1]['rating'])

    all_ratings = [movie_info["rating"] for movie_info in movies.values()]
    median_rating = statistics.median(all_ratings)

    results = [
        f"Best movie: {best_movie_name} - {best_movie_info['rating']}",
        f"Worst movie: {worst_movie_name} - {worst_movie_info['rating']}",
        f"Median rating: {round(median_rating, 1)}",
        f"Average rating: {round((sum(all_ratings) / len(all_ratings)), 1)}",
    ]

    return {
        "type": "list",
        "color_code": "MENU",
        "data": results
    }


def get_rating_histogram(file_name):
    """Generate a rating histogram and save it to the given .jpg file."""
    movies = movie_db.list_movies()
    all_ratings = [movie_info["rating"] for movie_info in movies.values()]

    if not file_name or not file_name.endswith(".jpg"):
        raise ValueError("Invalid file name. Please enter a name ending with .jpg")

    try:
        plt.hist(all_ratings, bins=20, range=(0, 10))
        plt.xlabel("Rating")
        plt.ylabel("Number of movies")
        plt.title("Movie Ratings Distribution")
        plt.grid(True)

        plt.savefig(file_name)

    except Exception as e:
        print(color_text(f"Unexpected error: {e}", "ERROR"))

    finally:
        plt.close()

    return {
        "type": "message",
        "color_code": "SUCCESS",
        "data": f"Histogram will be saved in '{file_name}' momentarily."
    }


def generate_website():
    movie_data = movie_db.list_movies()
    with open(TEMPLATE_PATH, 'r') as fr:
        template_data = fr.read()
        html_output = html_generator.generate_html(template_data, "MovieVault 🍿", movie_data)
        with open(WEBSITE_OUTPUT_PATH, "w") as fw:
            fw.write(html_output)
    print("Website generated successfully!")