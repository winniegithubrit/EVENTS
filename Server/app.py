# app.py

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, Event, Partnership  # Import the SQLAlchemy instance and models

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

if __name__ == "__main__":
    app.run(debug=True)
