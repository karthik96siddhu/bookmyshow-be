from fastapi import FastAPI
from app.routes import admin_theatre, auth, screen, movie, admin_show

app = FastAPI()

#include auth routes
app.include_router(auth.router)
app.include_router(admin_theatre.router)
app.include_router(screen.router)
app.include_router(movie.router)
app.include_router(admin_show.router)

@app.get("/")
def root():
    return {"message": "Welcome to the BookMyShow API"}