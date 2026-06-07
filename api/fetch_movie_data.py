"""OMDB API client for fetching movie data."""

import os
import requests
from dotenv import load_dotenv

REQUEST_URL = "https://www.omdbapi.com"

load_dotenv()
API_KEY = os.environ.get("OMDB_API_KEY")


def fetch_movie_data(title):
    """Fetch movie details from the OMDB API by title."""
    params = {
        "apikey": API_KEY,
        "t": title
    }
    try:
        response = requests.get(REQUEST_URL, params=params)
        return response.json()
    except requests.exceptions.ConnectionError as err:
        print(f"There seems to be a connection error. Please check your internet connection: {err}")

    except requests.exceptions.Timeout as err:
        print(f"The API timed out. {err}")

    except requests.exceptions.HTTPError as err:
        print(f"The API is online, but sent back an HTTP error code: {err}")
        # Handle 500 (Server Error) or 403 (Forbidden), etc.

    except requests.exceptions.RequestException as err:
        print(f"A catastrophic, unknown requests error occurred: {err}")