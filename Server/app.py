import firebase_admin
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, Event, Partnership  
from dotenv import load_dotenv
from firebase import bucket
from firebase_admin import credentials, storage  
from user import userBlueprint
from partnership import partnershipBlueprint

import os

load_dotenv()
FIREBASE_KEY_PATH = os.getenv('FIREBASE_KEY_PATH')
FIREBASE_BUCKET_NAME = os.getenv('FIREBASE_BUCKET_NAME')

if not firebase_admin._apps: 
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_BUCKET_NAME
    })


# Initialize the migration tool
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    # Initialize the database and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)
    # registering blueprints
    app.register_blueprint(userBlueprint)
    app.register_blueprint(partnershipBlueprint)

    with app.app_context():
        # Create all tables
        db.create_all()

    return app

app = create_app()

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!", 200

@app.route('/')
def index():
    return {"message": "success"}

@app.route('/events', methods=['GET'])
def get_all_events():
    try:
        events = Event.query.all()
        event_list = [event.to_dict() for event in events]
        return jsonify(event_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# get events by id
@app.route('/events/<int:event_id>', methods=['GET'])
def get_events_by_id(event_id):
    event = Event.query.get(event_id)
    if event:
        return jsonify(event.to_dict()), 200
    else:
        return jsonify({'error':'Event not found'}), 404
# created a new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.form
    image_file = request.files.get('image')  
    name = data.get('name')
    description = data.get('description')
    location = data.get('location')
    date = data.get('date')
    organizer_id = data.get('organizer_id') 
    if not organizer_id:
        return jsonify({'error': 'Organizer ID is required.'}), 400
    image_url = None

    if image_file:
        blob = bucket.blob(image_file.filename)
        try:
            blob.upload_from_file(image_file, content_type=image_file.content_type)
            blob.make_public() 
            image_url = blob.public_url 
        except Exception as e:
            return jsonify({'error': f'Image upload failed: {str(e)}'}), 500

    # Creating a new event
    new_event = Event(
        image=image_url,
        name=name,
        description=description,
        location=location,
        date=date,
        organizer_id=organizer_id  
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.to_dict()), 201
# partially updating an event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    name = request.form.get('name')
    description = request.form.get('description')
    location = request.form.get('location')
    date = request.form.get('date')
    image = request.form.get('image')  
    if name:
        event.name = name
    if description:
        event.description = description
    if location:
        event.location = location
    if date:
        event.date = date
    if image:
        event.image = image  

    db.session.commit()
    return jsonify({'message': 'Event updated successfully', 'event': event.to_dict()}), 200

@app.route('/events/<int:event_id>', methods=['PUT'])
def replace_event(event_id):
    event = Event.query.get_or_404(event_id)
    # Accessing the form data
    name = request.form.get('name', event.name)
    description = request.form.get('description', event.description)  
    location = request.form.get('location', event.location)  
    date = request.form.get('date', event.date)  
    image = request.form.get('image', event.image) 
    event.name = name
    event.description = description
    event.location = location
    event.date = date
    event.image = image
    db.session.commit()
    return jsonify({'message': 'Event replaced successfully', 'event': event.to_dict()}), 200

# Deleting an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.image:
        file_name = event.image.split('/')[-1]  
        bucket = storage.bucket()
        blob = bucket.blob(file_name) 
        blob.delete() 
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 204



    
if __name__ == "__main__":
    app.run(debug=True)
