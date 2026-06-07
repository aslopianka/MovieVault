

def generate_html(template_data, title, movies_data):
    movie_items = []
    full_html = ""
    for movie_name, movie_data in movies_data.items():
        movie_html = f"""
         <li>
            <div class="movie">
                <img class="movie-poster"
                     src="{movie_data.get("poster_url")}"
                     alt="{movie_name}"/>
                <div class="movie-title">{movie_name}</div>
                <div class="movie-year">{movie_data.get("year", "-")}</div>
            </div>
         </li>
                    """
        movie_items.append(movie_html.strip())

    movie_grid_html = "\n".join(movie_items)
    full_html = template_data.replace("__TEMPLATE_TITLE__", title)
    full_html = full_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    return full_html
