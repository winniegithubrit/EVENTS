from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Many-to-many relationship between events and partnerships
event_partners = db.Table('event_partners',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('partnership_id', db.Integer, db.ForeignKey('partnership.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    billing = db.relationship('Billing', backref='user', lazy=True)
    events = db.relationship('Event', backref='organizer', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    partnerships = db.relationship('Partnership', backref='user', lazy=True)
    invoices = db.relationship('Invoice', backref='user', lazy=True)
    emails = db.relationship('Email', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at.isoformat()
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    billing = db.relationship('Billing', backref='event', lazy=True)
    reviews = db.relationship('Review', backref='event', lazy=True)
    calendar = db.relationship('Calendar', backref='event', lazy=True)
    invoices = db.relationship('Invoice', backref='event', lazy=True)

    associated_partnerships = db.relationship(
        'Partnership',
        secondary=event_partners,
        back_populates='events',
        overlaps='events_associated'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'date': self.date
        }

class Partnership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    partner_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    role = db.Column(db.String(200), nullable=True)

    events = db.relationship(
        'Event',
        secondary=event_partners,
        back_populates='associated_partnerships',
        overlaps='partnerships'
    )
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'partner_name': self.partner_name,
            'description': self.description,
            'role': self.role
        }

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # like paid or maybe pending
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "status": self.status,
            "user_id": self.user_id,
            "event_id": self.event_id
        }

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), unique=True, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # like paid or unpaid
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,  
            "invoice_number": self.invoice_number,
            "amount_due": self.amount_due,
            "due_date": self.due_date.isoformat(),  
            "status": self.status,
            "user_id": self.user_id,
            "event_id": self.event_id
        }

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return{
            "id": self.id,
            "subject":self.subject,
            "body": self.body,
            "recipient":self.recipient,
            "sent_at":self.sent_at.isoformat(),
            "user_id":self.user_id
        }

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "details": self.details
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) 
    comment = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "user_id": self.user_id,
            "event_id": self.event_id
        }
    
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "user_id": self.user_id,
            "event_id": self.event_id
        }

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "sent_at": self.sent_at.isoformat(),
            "is_read": self.is_read
        }

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    seat_number = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "purchase_date": self.purchase_date.isoformat(),
            "price": self.price,
            "seat_number": self.seat_number
        }

# This model enables users to share events with one another
class SocialIntegration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with = db.Column(db.String(120), nullable=False)  
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "shared_with": self.shared_with,
            "shared_at": self.shared_at.isoformat()
        }

class PartnershipDiscount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partnership.id'), nullable=False)
    image = db.Column(db.String, nullable=True)
    discount_amount = db.Column(db.Float, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            "id": self.id,
            "partner_id": self.partner_id,
            "image": self.image,
            "discount_amount": self.discount_amount,
            "event_id": self.event_id,
            "description": self.description
        }
