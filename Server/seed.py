import os
from faker import Faker
from app import app, db, Event  

fake = Faker()

def create_fake_events(num_events):
    for _ in range(num_events):
        event = Event(
            image=fake.image_url(),
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            location=fake.city(),
            date=fake.date_time_between(start_date='now', end_date='+30d'),
            organizer_id=fake.random_int(min=1, max=10)  
        )
        db.session.add(event)
    db.session.commit()
    print(f'{num_events} fake events created!')

if __name__ == '__main__':
    with app.app_context():
        create_fake_events(20)  
