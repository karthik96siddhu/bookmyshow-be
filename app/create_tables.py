from app.db.database import Base, engine

# Import all models here
from app.models.user import User
from app.models.theatre import Theatre
from app.models.screen import Screen
from app.models.movie import Movie
from app.models.show import Show
from app.models.seat import Seat
from app.models.booking import Booking
from app.models.seat_lock import SeatLock

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Done!")
