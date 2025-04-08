from repositories.base_repository import BaseRepository
from models.movie import Movie, MovieCreate

class MovieRepository(BaseRepository):
    def get_all(self) -> list[Movie]:
        self.cursor.execute("SELECT * FROM MOVIE")
        return [Movie.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def get_by_id(self, movie_id: int) -> Movie | None:
        self.cursor.execute("SELECT * FROM MOVIE WHERE movie_id = ?", (movie_id,))
        row = self.cursor.fetchone()
        return Movie.model_validate(dict(row)) if row else None

    def create(self, movie: MovieCreate) -> int:
        self.cursor.execute(
            "INSERT INTO MOVIE (title, genre, language, duration) VALUES (?, ?, ?, ?)",
            (movie.title, movie.genre, movie.language, movie.duration)
        )
        return self.cursor.lastrowid

    def update(self, movie_id: int, title: str | None = None, genre: str | None = None, 
               language: str | None = None, duration: int | None = None) -> bool:
        updates = {k: v for k, v in {"title": title, "genre": genre, "language": language, "duration": duration}.items() if v is not None}
        if not updates:
            return False
        query = "UPDATE MOVIE SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE movie_id = ?"
        self.cursor.execute(query, list(updates.values()) + [movie_id])
        return self.cursor.rowcount > 0

    def delete(self, movie_id: int) -> bool:
        self.cursor.execute("DELETE FROM MOVIE WHERE movie_id = ?", (movie_id,))
        return self.cursor.rowcount > 0