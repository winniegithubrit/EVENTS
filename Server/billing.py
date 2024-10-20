from flask import Blueprint, request, jsonify
from models import Billing, db

billingBlueprint = Blueprint('billing', __name__)

@billingBlueprint.route('/billing', methods=['GET'])
def get_all_billing():
    billings = Billing.query.all()
    billing_list = [billing.to_dict() for billing in billings ]
    return jsonify(billing_list)

@billingBlueprint.route('/billing/<int:billing_id>', methods=['GET'])
def get_billing_by_id(billing_id):
    billing = Billing.query.get(billing_id)
    if billing:
        return jsonify(billing.to_dict()), 200
    else:
        return jsonify({'error':'Billing not found'})
    
# create a new billing
@billingBlueprint.route('/billing', methods=['POST'])
def create_billing():
    data = request.get_json()
    new_billing = Billing(
        amount = data['amount'],
        status = data['status'],
        user_id = data['user_id'],
        event_id = data['event_id']
    )
    db.session.add(new_billing)
    db.session.commit()
    return jsonify(new_billing.to_dict()), 201


# patch a billing
@billingBlueprint.route('/billing/<int:billing_id>', methods=['PATCH'])
def update_billing(billing_id):
    data = request.get_json()

    billing = Billing.query.get(billing_id)
    
    if not billing:
        return jsonify({'error': 'Billing record not found'}), 404

    if 'amount' in data:
        billing.amount = data['amount']
    if 'status' in data:
        billing.status = data['status']

    db.session.commit()
    
    return jsonify({'message': 'Billing updated successfully', 'billing': billing.to_dict()}), 200


# put a billing
@billingBlueprint.route('/billing/<int:billing_id>', methods=['PUT'])
def put_billing(billing_id):
    data = request.get_json()

    billing = Billing.query.get(billing_id)
    
    if not billing:
        return jsonify({'error': 'Billing record not found'}), 404

    if 'amount' in data:
        billing.amount = data['amount']
    if 'status' in data:
        billing.status = data['status']

    db.session.commit()
    
    return jsonify({'message': 'Billing updated successfully', 'billing': billing.to_dict()}), 200

# delete a billing
@billingBlueprint.route('/billing/<int:billing_id>', methods=['DELETE'])
def delete_billing(billing_id):
    billing = Billing.query.get_or_404(billing_id)
    db.session.delete(billing)
    db.session.commit()
    return jsonify({'message': 'Billing deleted successfully'}), 204

    
    