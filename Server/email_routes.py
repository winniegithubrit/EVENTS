# email_routes.py
from flask import Blueprint, jsonify, request
from models import Email, db
from flask_mail import Message
from datetime import datetime

emailRouteBluePrint = Blueprint('email', __name__)

@emailRouteBluePrint.route('/emails', methods=['GET'])
def get_all_emails():
    emails = Email.query.all()
    email_list = [email.to_dict() for email in emails]
    return jsonify(email_list), 200  

@emailRouteBluePrint.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    subject = data.get('subject')
    body = data.get('body')
    recipient = data.get('recipient')
    user_id = data.get('user_id')  

    # Validate the incoming data
    if not subject or not body or not recipient:
        return jsonify({'error': 'Subject, body, and recipient are required.'}), 400

    # Create and send the email
    msg = Message(subject, recipients=[recipient])
    msg.body = body

    try:
        emailRouteBluePrint.mail.send(msg)  # Use the mail instance from the blueprint
        new_email = Email(
            subject=subject,
            body=body,
            recipient=recipient,
            sent_at=datetime.utcnow(),  
            user_id=user_id  
        )
        db.session.add(new_email)
        db.session.commit()

        return jsonify({'message': 'Email sent successfully!', 'sent_at': new_email.sent_at.isoformat()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@emailRouteBluePrint.route('/emails', methods=['POST'])
def create_email():
    data = request.get_json()
    
    new_email = Email(
        subject=data['subject'],
        body=data['body'],
        recipient=data['recipient'],
        user_id=data['user_id']
    )
    
    db.session.add(new_email)
    db.session.commit()
    
    response = {
        "message": "Email created successfully!",
        "email": new_email.to_dict()
    }
    
    return jsonify(response), 201

@emailRouteBluePrint.route('/emails/<int:email_id>', methods=['PATCH'])
def update_email(email_id):
    email = Email.query.get_or_404(email_id)
    data = request.get_json()

    if 'subject' in data:
        email.subject = data['subject']
    if 'body' in data:
        email.body = data['body']
    if 'recipient' in data:
        email.recipient = data['recipient']

    db.session.commit()
    return jsonify(email.to_dict()), 200

@emailRouteBluePrint.route('/emails/<int:email_id>', methods=['PUT'])
def replace_email(email_id):
    data = request.get_json()
    email = Email.query.get_or_404(email_id)

    email.subject = data['subject']
    email.body = data['body']
    email.recipient = data['recipient']
    email.user_id = data['user_id']

    db.session.commit()
    return jsonify(email.to_dict()), 200

@emailRouteBluePrint.route('/emails/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    email = Email.query.get_or_404(email_id)
    db.session.delete(email)
    db.session.commit()
    return jsonify({"message": "Email deleted successfully."}), 204

