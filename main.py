import csv
from models import Movie, Watchlist

DATA_FILE = "data/movies.csv"


def load_movies(path):
    movies = []
    try:
        with open(path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for line_no, row in enumerate(reader, start=2):
                try:
                    movies.append(Movie(row["title"].strip(), row["genre"].strip(),
                                        float(row["rating"]), int(row["duration"])))
                except (ValueError, KeyError, AttributeError, TypeError) as err:
                    print(f"[WARNING] Skipping bad row at line {line_no}: {err}")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
    return movies


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Invalid input! Please enter a number (e.g. 8.0).")


def show(movies, empty_msg="No movies found."):
    if not movies:
        print(empty_msg)
        return
    for i, movie in enumerate(movies, start=1):
        print(f"{i:>2}. {movie}")


def find_movie(movies, title):
    matches = [m for m in movies if m.title.lower() == title.strip().lower()]
    return matches[0] if matches else None


def show_menu():
    print("\n===== MOVIE NIGHT PLANNER =====")
    print("1. View all movies")
    print("2. Search by genre")
    print("3. Filter by minimum rating")
    print("4. Add movie to watchlist")
    print("5. Remove movie from watchlist")
    print("6. View watchlist")
    print("7. Watchlist analytics")
    print("0. Exit")


def main():
    movies = load_movies(DATA_FILE)
    if not movies:
        print("No movies loaded. Exiting.")
        return
    print(f"Loaded {len(movies)} movies from {DATA_FILE}")
    watchlist = Watchlist()

    while True:
        show_menu()
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            break

        if choice == "1":
            show(movies)
        elif choice == "2":
            genre = input("Enter genre: ").strip().lower()
            show([m for m in movies if m.genre.lower() == genre],
                 f"No movies in genre '{genre}'.")
        elif choice == "3":
            min_rating = read_float("Minimum rating: ")
            show([m for m in movies if m.rating >= min_rating],
                 f"No movies with rating >= {min_rating}.")
        elif choice == "4":
            movie = find_movie(movies, input("Movie title to add: "))
            if movie is None:
                print("Movie not found in library.")
            elif watchlist.add(movie):
                print(f"Added '{movie.title}' to watchlist.")
            else:
                print(f"'{movie.title}' is already in your watchlist!")
        elif choice == "5":
            title = input("Movie title to remove: ")
            print("Removed." if watchlist.remove(title) else "Not in your watchlist.")
        elif choice == "6":
            show(watchlist.get_movies(), "Your watchlist is empty.")
        elif choice == "7":
            if len(watchlist) == 0:
                print("Watchlist is empty. Add movies first.")
            else:
                total = watchlist.total_duration()
                print(f"Movies in watchlist : {len(watchlist)}")
                print(f"Total duration      : {total} min ({total // 60}h {total % 60}m)")
                print(f"Average rating      : {watchlist.average_rating():.2f}")
        elif choice == "0":
            break
        else:
            print("Invalid option. Choose 0-7.")
    print("Enjoy your movie night!")


if __name__ == "__main__":
    main()