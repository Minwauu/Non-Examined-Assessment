from flask_sqlalchemy import SQLAlchemy, Enum
from flask_login import UserMixin
from extensions import db
from datetime import datetime

# user model (admin + customers for now maybe add accessability users)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)

# movie model

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True, nullable =False)
    duration = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable=False)
    screenings = db.relationship('Screening', backref = 'movie', lazy = True)

# screenings 

class Screening(db.Modeld):
    id = db.Column(db.Integer, primary_key = True)
    screen_number = db.Column(db.Integer, nullable = False)
    movie_id = db.Column(db.Integer, db.ForeignLey('movie.id'), nullable=False) # maybe used in favourites
    showtimes = db.relationship('Showtime', backref = 'screening', lazy = True)

# showings

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime, nullable=False)
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'), nullable = False) #will be used in bookings

#bookings and status

class SeatStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    BOOKED = "booked"
    ACCESSIBLE_AVAILABLE = "accessible_available"
    ACCESSIBLE_RESERVED = "accessible_reserved"
    ACCESSIBLE_BOOKED = "accessible_booked"
    UNAVAILABLE = "unavailable"


class SeatBooking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    seat_number = db.Column(db.String(10), nullable = False)
    status = db.Column(db.Boolean, default = True, nullable = False)
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    accessability = db.Column(db.Boolean, default = True, nullable=False)
    screening = db.relationship("Screening", backref = "seatbooking")
    user = db.relationship("User", backref = "bookings") 




