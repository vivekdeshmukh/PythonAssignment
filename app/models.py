from app import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    booking_count = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        # Convert the object fields to a dictionary that is JSON serializable
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'booking_count': self.booking_count,
            'date_joined': self.date_joined.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
        }

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    remaining_count = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        # Convert the object fields to a dictionary that is JSON serializable
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'remaining_count': self.remaining_count,
            'expiration_date': self.expiration_date.strftime('%d/%m/%Y')  # Convert datetime to string
        }

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now(datetime.now().astimezone().tzinfo))
    
    member = db.relationship('Member', back_populates="bookings")
    inventory = db.relationship('Inventory', back_populates="bookings")

Member.bookings = db.relationship('Booking', back_populates='member')
Inventory.bookings = db.relationship('Booking', back_populates='inventory')
