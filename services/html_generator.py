import os
import shutil


def generate_html(template_data, title, movies_data):
    # needs to happen here because /dist is in .gitignore
    os.makedirs("dist", exist_ok=True)
    shutil.copy("templates/style.css", "dist/style.css")

    movie_items = []
    full_html = ""
    for movie_name, movie_data in movies_data.items():
        movie_html = f"""
         <li>
            <div class="movie">
                <a href="https://www.imdb.com/title/{movie_data.get('imdbID')}/" target="_blank"> 
                    <img class="movie-poster"
                         src="{movie_data.get("poster_url")}"
                         alt="{movie_name}"/>
                </a>
                <div class="movie-title">{movie_name}</div>
                <div class="movie-rating">Rating: {movie_data.get("rating", "-")}</div>
                <div class="movie-year">{movie_data.get("year", "-")}</div>
                
            </div>
         </li>
                    """
        movie_items.append(movie_html.strip())

    movie_grid_html = "\n".join(movie_items)
    full_html = template_data.replace("__TEMPLATE_TITLE__", title)
    full_html = full_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    return full_html
