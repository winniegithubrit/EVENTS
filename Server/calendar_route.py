from flask import Blueprint, jsonify, request
from models import Calendar, db
from datetime import datetime

calendarBluePrint = Blueprint('calendar', __name__)

@calendarBluePrint.route('/calendars', methods=['GET'])
def get_all_calendars():
    calendars = Calendar.query.all()
    return jsonify([calendar.to_dict() for calendar in calendars]), 200

@calendarBluePrint.route('/calendars/<int:id>', methods=['GET'])
def get_calendar_by_id(calendar_id):
    calendar = Calendar.query.get(calendar_id)
    if calendar is None:
        return jsonify({"message": "Calendar not found"}), 404
    return jsonify(calendar.to_dict()), 200

@calendarBluePrint.route('/calendars', methods=['POST'])
def create_calendar():
    data = request.get_json()
    new_calendar = Calendar(
        event_id=data['event_id'],
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        details=data.get('details')  
    )
    
    db.session.add(new_calendar)
    db.session.commit()
    
    response = {
        "message": "Calendar created successfully!",
        "calendar": new_calendar.to_dict()
    }
    
    return jsonify(response), 201

@calendarBluePrint.route('/calendars/<int:id>', methods=['PATCH'])
def update_calendar(calendar_id):
    calendar = Calendar.query.get(calendar_id)
    if calendar is None:
        return jsonify({"message": "Calendar not found"}), 404

    data = request.get_json()
    
    if 'event_id' in data:
        calendar.event_id = data['event_id']
    if 'start_time' in data:
        calendar.start_time = datetime.fromisoformat(data['start_time'])
    if 'end_time' in data:
        calendar.end_time = datetime.fromisoformat(data['end_time'])
    if 'details' in data:
        calendar.details = data['details']
    
    db.session.commit()

    response = {
        "message": "Calendar updated successfully!",
        "calendar": calendar.to_dict()
    }
    
    return jsonify(response), 200

@calendarBluePrint.route('/calendars/<int:id>', methods=['DELETE'])
def delete_calendar(calendar_id):
    calendar = Calendar.query.get(calendar_id)
    if calendar is None:
        return jsonify({"message": "Calendar not found"}), 404
    
    db.session.delete(calendar)
    db.session.commit()
    
    return jsonify({"message": "Calendar deleted successfully!"}), 204
