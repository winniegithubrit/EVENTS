from flask import Blueprint, jsonify, request
from models import PartnershipDiscount, db

partnershipDiscountBlueprint = Blueprint('partnershipDiscount', __name__)

@partnershipDiscountBlueprint.route('/partnershipDiscount', methods=['GET'])
def get_partnershipDiscounts():
    discounts = PartnershipDiscount.query.all()
    return jsonify([discount.to_dict() for discount in discounts])

@partnershipDiscountBlueprint.route('/partnershipDiscount/<int:discount_id>', methods=['GET'])
def get_partnershipDiscount_by_id(discount_id):
    discount = PartnershipDiscount.query.get(discount_id)
    if discount is None:
        return jsonify({"message": "Discount not found"}), 404
    return jsonify(discount.to_dict()), 200

@partnershipDiscountBlueprint.route('/partnershipDiscount', methods=['POST'])
def create_partnershipDiscount():
    data = request.get_json()
    new_discount = PartnershipDiscount(
        partner_id=data['partner_id'],
        image=data['image'],
        discount_amount=data['discount_amount'],
        event_id=data['event_id'],
        description=data['description']
    )
    db.session.add(new_discount)
    db.session.commit()
    return jsonify(new_discount.to_dict()), 201

@partnershipDiscountBlueprint.route('/partnershipDiscount/<int:discount_id>', methods=['PUT'])
def update_partnershipDiscount(discount_id):
    data = request.get_json()
    discount = PartnershipDiscount.query.get(discount_id)
    if discount is None:
        return jsonify({"message": "Discount not found"}), 404
    if 'partner_id' in data:
        discount.partner_id = data['partner_id']
    if 'image' in data:
        discount.image = data['image']
    if 'discount_amount' in data:
        discount.discount_amount = data['discount_amount']
    if 'event_id' in data:
        discount.event_id = data['event_id']
    if 'description' in data:
        discount.description = data['description']
    db.session.commit()
    return jsonify(discount.to_dict()), 200

@partnershipDiscountBlueprint.route('/partnershipDiscount/<int:discount_id>', methods=['PATCH'])
def patch_partnershipDiscount(discount_id):
    data = request.get_json()
    discount = PartnershipDiscount.query.get(discount_id)
    if 'partner_id' in data:
        discount.partner_id = data['partner_id']
    if 'image' in data:
        discount.image = data['image']
    if 'discount_amount' in data:
        discount.discount_amount = data['discount_amount']
    if 'event_id' in data:
        discount.event_id = data['event_id']
    if 'description' in data:
        discount.description = data['description']
    db.session.commit()
    return jsonify(discount.to_dict()), 200

@partnershipDiscountBlueprint.route('/partnershipDiscount/<int:discount_id>', methods=['DELETE'])
def delete_partnershipDiscount(discount_id):
    discount = PartnershipDiscount.query.get(discount_id)
    if discount is None:
        return jsonify({"message": "Discount not found"}), 404
    db.session.delete(discount)
    db.session.commit()
    return jsonify({"message": "Discount deleted successfully!"}), 204