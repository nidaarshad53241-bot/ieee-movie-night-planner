class Movie:
    def __init__(self, title, genre, rating, duration):
        self.title = title
        self.genre = genre
        self.rating = float(rating)
        self.duration = int(duration)

    def get_details(self):
        return (f"{self.title:<22} | {self.genre:<10} | "
                f"Rating: {self.rating:<4} | {self.duration} min")

    def __str__(self):
        return self.get_details()


class Watchlist:
    def __init__(self):
        self._movies = []
        self._titles = set()

    def add(self, movie):
        key = movie.title.lower()
        if key in self._titles:
            return False
        self._titles.add(key)
        self._movies.append(movie)
        return True

    def remove(self, title):
        key = title.strip().lower()
        if key not in self._titles:
            return False
        self._titles.remove(key)
        self._movies = [m for m in self._movies if m.title.lower() != key]
        return True

    def get_movies(self):
        return list(self._movies)

    def total_duration(self):
        return sum(m.duration for m in self._movies)

    def average_rating(self):
        if not self._movies:
            return 0.0
        return sum(m.rating for m in self._movies) / len(self._movies)

    def __len__(self):
        return len(self._movies)