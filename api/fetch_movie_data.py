"""OMDB API client for fetching movie data."""

import os
import requests
from dotenv import load_dotenv

REQUEST_URL = "https://www.omdbapi.com"

load_dotenv()
API_KEY = os.environ.get("OMDB_API_KEY")


def fetch_movie_data(title):
    """Fetch movie details from the OMDB API by title.

    Always returns a dict. On success, the OMDB JSON response. On failure,
    a dict shaped like OMDB's own error response so callers can handle both
    cases the same way: {"Response": "False", "Error": "<message>"}.
    """
    params = {
        "apikey": API_KEY,
        "t": title
    }
    try:
        response = requests.get(REQUEST_URL, params=params)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"Response": "False", "Error": "Connection error. Please check your internet connection."}

    except requests.exceptions.Timeout:
        return {"Response": "False", "Error": "The movie service timed out. Please try again."}

    except requests.exceptions.HTTPError as err:
        # Handle 500 (Server Error) or 403 (Forbidden), etc.
        return {"Response": "False", "Error": f"The movie service returned an error: {err}"}

    except requests.exceptions.RequestException as err:
        return {"Response": "False", "Error": f"An unexpected error occurred: {err}"}