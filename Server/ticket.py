from flask import Blueprint, request, jsonify
from models import Ticket, db

ticketBlueprint = Blueprint('ticket', __name__)

@ticketBlueprint.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([ticket.to_dict() for ticket in tickets])    

@ticketBlueprint.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket_by_id(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404
    return jsonify(ticket.to_dict()), 200

@ticketBlueprint.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    new_ticket = Ticket(
        event_id=data['event_id'],
        user_id=data['user_id'],
        purchase_date=data['purchase_date'],
        price=data['price'],
        seat_number=data['seat_number']
    )
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify(new_ticket.to_dict()), 201

@ticketBlueprint.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket_by_id(ticket_id):
    data = request.get_json()
    ticket = Ticket.query.get(ticket_id)
    ticket.event_id = data['event_id']
    ticket.user_id = data['user_id']
    ticket.purchase_date = data['purchase_date']
    ticket.price = data['price']
    ticket.seat_number = data['seat_number']
    db.session.commit()
    return jsonify(ticket.to_dict()), 200

@ticketBlueprint.route('/tickets/<int:ticket_id>', methods=['PATCH'])
def patch_ticket(ticket_id):
    data = request.get_json()
    ticket = Ticket.query.get(ticket_id)

    if 'event_id' in data:
        ticket.event_id = data['event_id']
    if 'user_id' in data:
        ticket.user_id = data['user_id']
    if 'purchase_date' in data:
        ticket.purchase_date = data['purchase_date']
    if 'price' in data:
        ticket.price = data['price']
    if 'seat_number' in data:
        ticket.seat_number = data['seat_number']

    db.session.commit()
    return jsonify(ticket.to_dict()), 200

@ticketBlueprint.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket deleted successfully"}), 200