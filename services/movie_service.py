from database.connection import get_db
from repositories.movie_repository import MovieRepository
from models.movie import Movie, MovieCreate

class MovieService:
    @staticmethod
    def get_all_movies() -> list[Movie]:
        with get_db() as conn:
            repo = MovieRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_movie(movie_id: int) -> Movie:
        with get_db() as conn:
            repo = MovieRepository(conn)
            movie = repo.get_by_id(movie_id)
            if not movie:
                raise ValueError("Movie not found")
            return movie

    @staticmethod
    def add_movie(movie: MovieCreate, admin_id: int) -> int:
        with get_db() as conn:
            repo = MovieRepository(conn)
            movie_id = repo.create(movie)
            repo.commit()
            AuditService.log_action(admin_id, "ADD", "MOVIE", movie_id, f"Added movie: {movie.title}")
            return movie_id

    @staticmethod
    def update_movie(movie_id: int, title: str | None, genre: str | None, language: str | None, 
                     duration: int | None, admin_id: int) -> bool:
        with get_db() as conn:
            repo = MovieRepository(conn)
            if not repo.update(movie_id, title, genre, language, duration):
                raise ValueError("Movie not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "MOVIE", movie_id, "Updated movie details")
            return True

    @staticmethod
    def delete_movie(movie_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = MovieRepository(conn)
            if not repo.delete(movie_id):
                raise ValueError("Movie not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "MOVIE", movie_id, "Deleted movie")
            return True