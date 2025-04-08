from fastapi import APIRouter, Depends, HTTPException
from services.show_service import ShowService
from models.show import Show, ShowCreate, ShowUpdate
from routes.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list[Show])
async def get_shows():
    return ShowService.get_all_shows()

@router.get("/{show_id}", response_model=Show)
async def get_show(show_id: int):
    try:
        return ShowService.get_show(show_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/movie/{movie_id}", response_model=list[Show])
async def get_shows_by_movie(movie_id: int):
    return ShowService.get_shows_by_movie(movie_id)

@router.get("/screen/{screen_id}", response_model=list[Show])
async def get_shows_by_screen(screen_id: int):
    return ShowService.get_shows_by_screen(screen_id)

@router.post("/", status_code=201)
async def create_show(show: ShowCreate, user=Depends(get_current_admin)):
    try:
        show_id = ShowService.create_show(show, user["user_id"])
        return {"message": "Show created", "show_id": show_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{show_id}")
async def update_show(show_id: int, update: ShowUpdate, user=Depends(get_current_admin)):
    try:
        ShowService.update_show(show_id, update, user["user_id"])
        return {"message": "Show updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{show_id}")
async def delete_show(show_id: int, user=Depends(get_current_admin)):
    try:
        ShowService.delete_show(show_id, user["user_id"])
        return {"message": "Show deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))