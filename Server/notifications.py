from flask import Blueprint, request, jsonify
from models import Notification, db

notificationBlueprint = Blueprint('notification', __name__)

@notificationBlueprint.route('/notification', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([notification.to_dict() for notification in notifications]), 200

@notificationBlueprint.route('/notification/<int:notification_id>', methods=['GET'])
def get_notification_by_id(notification_id):
    notification = Notification.query.get(notification_id)  
    if notification is None:
        return jsonify({"message": "Notification not found"}), 404
    return jsonify(notification.to_dict()), 200

@notificationBlueprint.route('/notification', methods=['POST'])
def create_notification():
    data = request.get_json()
    new_notification = Notification(
        message=data['message'],
        user_id=data['user_id'],
        event_id=data['event_id']
    )
    db.session.add(new_notification)
    db.session.commit()
    return jsonify(new_notification.to_dict()), 201

@notificationBlueprint.route('/notification/<int:notification_id>', methods=['PATCH'])
def update_notification(notification_id):
    data = request.get_json()
    notification = Notification.query.get(notification_id)
    notification.message = data['message']
    notification.user_id = data['user_id']
    notification.event_id = data['event_id']
    db.session.commit()
    return jsonify(notification.to_dict()), 200  

@notificationBlueprint.route('/notification/<int:notification_id>', methods=['PUT'])
def update_notification_by_id(notification_id):
    data = request.get_json()    
    notification = Notification.query.get(notification_id)
    notification.message = data['message']
    notification.user_id = data['user_id']
    notification.event_id = data['event_id']
    db.session.commit()
    return jsonify(notification.to_dict()), 200   

@notificationBlueprint.route('/notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if notification is None:
        return jsonify({"message": "Notification not found"}), 404
    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted"}), 200