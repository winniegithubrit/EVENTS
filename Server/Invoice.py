from flask import Blueprint, request, jsonify
from models import Invoice, db

invoiceBlueprint = Blueprint('invoice', __name__)

@invoiceBlueprint.route('/invoice', methods=['GET'])
def get_all_invoices():
    print("Received request for all invoices")  
    invoices = Invoice.query.all()
    invoice_list = [invoice.to_dict() for invoice in invoices]
    return jsonify(invoice_list)

@invoiceBlueprint.route('/invoice/<int:invoice_id>', methods=['GET'])
def get_invoice_by_id(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if invoice:
        return jsonify(invoice.to_dict()), 200
    else:
        return jsonify({'error':'Invoice not found'})
    
@invoiceBlueprint.route('/invoice', methods=['POST'])
def create_invoice():
    data = request.get_json()
    invoice = Invoice(
        invoice_number=data['invoice_number'],
        amount_due=data['amount_due'],
        due_date=data['due_date'],
        status=data['status'],
        user_id=data['user_id'],
        event_id=data['event_id']
    )
    db.session.add(invoice)
    db.session.commit()
    return jsonify(invoice.to_dict())

@invoiceBlueprint.route('/invoice/<int:invoice_id>', methods=['PATCH'])
def patch_invoice(invoice_id):
    data = request.get_json()
    invoice = Invoice.query.get_or_404(invoice_id)
    if invoice:
        if 'invoice_number' in data:
            invoice.invoice_number = data['invoice_number']
        if 'amount_due' in data:
            invoice.amount_due = data['amount_due']
        if 'due_date' in data:
            invoice.due_date = data['due_date']
        if 'status' in data:
            invoice.status = data['status']
        if 'user_id' in data:
            invoice.user_id = data['user_id']
        if 'event_id' in data:
            invoice.event_id = data['event_id']
        db.session.commit()
        return jsonify(invoice.to_dict()), 200
    else:
        return jsonify({'error': 'Invoice not found'}), 404

@invoiceBlueprint.route('/invoice/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    data = request.get_json()
    invoice = Invoice.query.get_or_404(invoice_id)
    if invoice:
        invoice.invoice_number = data['invoice_number']
        invoice.amount_due = data['amount_due']
        invoice.due_date = data['due_date']
        invoice.status = data['status']
        invoice.user_id = data['user_id']
        invoice.event_id = data['event_id']
        db.session.commit()
        return jsonify(invoice.to_dict()), 200
    else:
        return jsonify({'error': 'Invoice not found'}), 404

@invoiceBlueprint.route('/invoice/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    if invoice:
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({'message': 'Invoice deleted successfully'}), 200
    else:
        return jsonify({'error': 'Invoice not found'}), 404