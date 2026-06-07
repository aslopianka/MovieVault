"""CLI entry point for the movie database application."""

from services.logic import add_movie, delete_movie, get_random_movie, update_movie, search_movie, get_stats, \
    get_movies_sorted_by_rating, get_rating_histogram, list_movies, get_movies_sorted_chronologically, generate_website
from db.movie_storage_sql import init_db
from utils import color_text


def get_menu(title, show_title=True):
    """Build and return the list of formatted menu lines."""
    menu = []

    if show_title:
        menu.append(color_text(f"********** {title} **********", "MENU"))

    menu.extend([
        color_text("0  - Quit", "MENU"),
        color_text("1  - List movies", "MENU"),
        color_text("2  - Add movie", "MENU"),
        color_text("3  - Delete movie", "MENU"),
        color_text("4  - Update movie", "MENU"),
        color_text("5  - Stats", "MENU"),
        color_text("6  - Random movie", "MENU"),
        color_text("7  - Search movie", "MENU"),
        color_text("8  - Movies sorted by rating", "MENU"),
        color_text("9  - Movies sorted chronologically", "MENU"),
        color_text("10 - Create rating histogram", "MENU"),
        color_text("11 - Generate website", "MENU"),
    ])

    return menu


def get_valid_input():
    """
        Stays in a loop until the user provides valid data.
        Returns the title
        """
    while True:
         try:
             title =  input(color_text("Enter the name of the movie: ", "INPUT"))
             if not title:
                 raise ValueError("Title cannot be empty.")

             return title

         except ValueError as e:
             print(color_text(f"{e}", "ERROR"))


def get_valid_sorting_direction():
    """Prompt the user until a valid sorting direction ('ASC' or 'DESC') is entered."""
    while True:
        try:
            direction = input(color_text("Enter 'ASC' for ascending order or 'DESC' for descending order. ", "INPUT"))
            if direction.upper() in ["ASC", "DESC"]:
                return direction.upper()
            else:
                raise ValueError("Invalid sorting direction. Please enter 'ASC' or 'DESC'.")

        except ValueError as e:
            print(color_text(f"{e}", "ERROR"))


def get_corresponding_action(choice):
    """Return the action callable for the given menu choice."""
    actions = {
        1: lambda: list_movies(),
        2: lambda: add_movie(
            get_valid_input()
        ),
        3: lambda: delete_movie(
            input(color_text("Which movie do you want to delete? ", "INPUT"))
        ),
        4: lambda: update_movie(
            *get_valid_input()
        ),
        5: lambda: get_stats(),
        6: lambda: get_random_movie(),
        7: lambda: search_movie(
            input(color_text("Enter part of movie name: ", "INPUT"))
        ),
        8: lambda: get_movies_sorted_by_rating(),
        9: lambda: get_movies_sorted_chronologically(get_valid_sorting_direction()),
        10: lambda: get_rating_histogram(
            input(color_text("Enter the name of the file to save the histogram (.jpg): ", "INPUT"))
        ),
        11: lambda: generate_website()
    }

    if choice not in actions:
        raise ValueError("Invalid choice")

    return actions[choice]


def main():
    """Initialize the database and run the interactive menu loop."""
    init_db()
    title = "My Movies Database"
    first_run = True

    while True:
        menu = get_menu(title, show_title= first_run)
        first_run = False

        for line in menu:
            print(line)

        users_menu_choice = input(color_text("Enter your choice (1-9):\n", "INPUT"))

        try:
            users_choice = int(users_menu_choice)
        except ValueError:
            print(color_text("Invalid choice. Please only enter a number between 1 and 9.", "ERROR"))
            continue

        try:
            if users_choice == 0:
                print(color_text("Good bye!", "SUCCESS"))
                break

            else:
                action = get_corresponding_action(users_choice)
                result = action()

                if result is None:
                    pass
                elif result["type"] == "message":
                    print(color_text(result["data"], result["color_code"]))
                elif result["type"] == "list":
                    for item in result["data"]:
                        print(color_text(item, "MENU"))
                else:
                    print(color_text(result["data"], "INPUT"))

        except (ValueError, KeyError, TypeError) as e:
            print(color_text(str(e), "ERROR"))
            continue

        input(color_text("\nAction completed. Press Enter to continue...\n", "INPUT"))


if __name__ == "__main__":
    main()
