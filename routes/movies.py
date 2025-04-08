from fastapi import APIRouter, Depends, HTTPException
from services.movie_service import MovieService
from models.movie import Movie, MovieCreate
from routes.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list[Movie])
async def get_movies():
    return MovieService.get_all_movies()

@router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int):
    try:
        return MovieService.get_movie(movie_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", status_code=201)
async def add_movie(movie: MovieCreate, user=Depends(get_current_admin)):
    try:
        movie_id = MovieService.add_movie(movie, user["user_id"])
        return {"message": "Movie added", "movie_id": movie_id}
    except Exception:
        raise HTTPException(status_code=400, detail="Movie addition failed")

@router.put("/{movie_id}")
async def update_movie(movie_id: int, title: str | None = None, genre: str | None = None, 
                       language: str | None = None, duration: int | None = None, user=Depends(get_current_admin)):
    try:
        MovieService.update_movie(movie_id, title, genre, language, duration, user["user_id"])
        return {"message": "Movie updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, user=Depends(get_current_admin)):
    try:
        MovieService.delete_movie(movie_id, user["user_id"])
        return {"message": "Movie deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))