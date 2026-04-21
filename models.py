from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    shows = db.relationship('Showtime', backref='movie', lazy=True)

class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    shows = db.relationship('Showtime', backref='theater', lazy=True)

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # AC / Non-AC / Sleeper
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_seats = db.Column(db.Integer, default=40)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_number = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    classes = db.Column(db.String(100), nullable=False) # e.g. "SL, 3A, 2A"
    price_base = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_type = db.Column(db.String(50), nullable=False) # 'movie', 'bus', 'train'
    reference_id = db.Column(db.Integer, nullable=False) # ID of showtime, bus, or train
    seats = db.Column(db.String(100), nullable=False) # Comma separated
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending') # 'Pending', 'Confirmed'
    pnr = db.Column(db.String(20), nullable=True) # For trains
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
