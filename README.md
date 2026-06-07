# MovieVault

A command-line movie database application built with Python, SQLite, and SQLAlchemy.
You can add/search/update/delete movies, view stats, create a rating histogram, and generate a static movie website.

## Features

- Interactive CLI menu (`main.py`)
- SQLite-backed movie storage (`movies.db`) via SQLAlchemy
- Fetch movie metadata from the OMDb API when adding a movie
- Search movies by partial title
- View analytics:
  - best/worst movie
  - median and average ratings
  - rating histogram image export (`.jpg`)
- Generate a static HTML movie page in `dist/index.html`

## Tech Stack

- Python 3
- SQLAlchemy
- Requests
- python-dotenv
- Matplotlib (used for histogram generation)

## Project Structure

```text
movie_project/
├── api/
│   └── fetch_movie_data.py
├── db/
│   ├── movie_storage.py
│   └── movie_storage_sql.py
├── dist/
│   ├── index.html
│   └── style.css
├── services/
│   ├── html_generator.py
│   └── logic.py
├── templates/
│   └── index_template.html
├── main.py
├── movies.db
├── requirements.txt
└── utils.py
```

## Setup

1. **Clone the repository** and go to the project folder.
2. **Create and activate a virtual environment** (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the project root with your OMDb API key:

```env
OMDB_API_KEY=your_api_key_here
```

> Get a free key from: `https://www.omdbapi.com/apikey.aspx`

## Running the App

Start the CLI:

```bash
python main.py
```

At startup, the app initializes the SQLite table if it does not exist.

## CLI Menu Actions

- `1` List movies
- `2` Add movie (fetches data from OMDb)
- `3` Delete movie
- `4` Update movie rating
- `5` Show stats
- `6` Pick random movie
- `7` Search movie
- `8` List movies sorted by rating
- `9` List movies sorted chronologically (`ASC` / `DESC`)
- `10` Create rating histogram (`.jpg`)
- `11` Generate website
- `0` Quit

## Website Generation

Selecting menu option `11` builds a static page from `templates/index_template.html` and saves output to:

- `dist/index.html`

Open `dist/index.html` in a browser to view the generated movie gallery.
