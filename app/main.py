from fastapi import FastAPI
from app.routes import auth

app = FastAPI()

#include auth routes
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to the BookMyShow API"}