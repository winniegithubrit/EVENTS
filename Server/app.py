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

import os

load_dotenv()
FIREBASE_KEY_PATH = os.getenv('FIREBASE_KEY_PATH')
FIREBASE_BUCKET_NAME = os.getenv('FIREBASE_BUCKET_NAME')

if not firebase_admin._apps:  # Check if any apps have been initialized
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

@app.route('/events', methods=['POST'])
def create_event():
    # Use request.form to get regular fields and request.files for the image
    data = request.form
    image_file = request.files.get('image')  # Key should be 'image'
    name = data.get('name')
    description = data.get('description')
    location = data.get('location')
    date = data.get('date')
    organizer_id = data.get('organizer_id')  # Capture organizer_id

    # Ensure organizer_id is present
    if not organizer_id:
        return jsonify({'error': 'Organizer ID is required.'}), 400

    # Initialize image_url as None
    image_url = None

    if image_file:
        # Upload image to Firebase and get the URL
        blob = bucket.blob(image_file.filename)
        try:
            blob.upload_from_file(image_file, content_type=image_file.content_type)
            blob.make_public()  # Make the file publicly accessible
            image_url = blob.public_url  # Get the public URL of the uploaded image
        except Exception as e:
            return jsonify({'error': f'Image upload failed: {str(e)}'}), 500

    # Create a new event object
    new_event = Event(
        image=image_url,
        name=name,
        description=description,
        location=location,
        date=date,
        organizer_id=organizer_id  # Ensure this field is set
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.to_dict()), 201

    
if __name__ == "__main__":
    app.run(debug=True)
