import os
from faker import Faker
from app import app, db
from datetime import datetime
import random
from models import User, Event, Partnership

fake = Faker()

def create_db():
    with app.app_context():
        db.create_all()

def seed_data():
    with app.app_context():
        users = []
        for _ in range(10):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password='hashed_password'
            )
            users.append(user)
            db.session.add(user)
        db.session.commit()

        events = []
        for user in users:
            for _ in range(2):
                event = Event(
                    image=fake.image_url(),
                    name=fake.catch_phrase(),
                    description=fake.text(),
                    location=fake.city(),
                    date=fake.date_time_between(start_date='now', end_date='+1y'),
                    organizer_id=user.id
                )
                events.append(event)
                db.session.add(event)
        db.session.commit()

        partnerships = []
        for user in users:
            partnership = Partnership(
                user_id=user.id,
                partner_name=fake.company(),
                description=fake.catch_phrase(),
                role=random.choice(['Sponsor', 'Partner', 'Collaborator'])
            )
            partnerships.append(partnership)
            db.session.add(partnership)
        db.session.commit()

if __name__ == "__main__":
    create_db()
    seed_data()
    print("Database seeded successfully!")
