from database import db
from datetime import datetime


class Bookings(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.userid'))
    user = db.relationship('Users', backref=db.backref('bookings', lazy=True))
    classroom = db.Column(db.String(255))
    title = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=datetime.now)
    cancelled_on = db.Column(db.DateTime)

    def __str__(self):
        return f'Booking {self.booking_id}: {self.title} by User {self.user_id}'

# Ensure to import the Users class where this Booking class is defined, if they are in separate modules.
