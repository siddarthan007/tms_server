from fastapi import FastAPI
from routes import auth, bookings, customers, movies, screens, seats, seat_layouts, shows, theatres, tickets, audit_logs, admin as admins
from database.init_db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Theatre Management System", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(movies.router, prefix="/movies", tags=["movies"])
app.include_router(screens.router, prefix="/screens", tags=["screens"])
app.include_router(seats.router, prefix="/seats", tags=["seats"])
app.include_router(seat_layouts.router, prefix="/seat_layouts", tags=["seat_layouts"])
app.include_router(shows.router, prefix="/shows", tags=["shows"])
app.include_router(theatres.router, prefix="/theatres", tags=["theatres"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(audit_logs.router, prefix="/audit_logs", tags=["audit_logs"])
app.include_router(admins.router, prefix="/admins", tags=["admins"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)