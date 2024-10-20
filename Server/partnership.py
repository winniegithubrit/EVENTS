from flask import Blueprint, request, jsonify
from models import Partnership, db  

partnershipBlueprint = Blueprint('partnership', __name__)
# get all partnerships
@partnershipBlueprint.route('/partnerships', methods=['GET'])
def get_all_partneships():
    partnerships = Partnership.query.all()
    parrtneship_list = [partnership.to_dict() for partnership in partnerships]
    return jsonify(parrtneship_list)
# get partnership by id
@partnershipBlueprint.route('/partnerships/<int:partnership_id>', methods=['GET'])
def get_partnership_by_id(partnership_id):
    partnership = Partnership.query.get(partnership_id)
    if partnership:
        return jsonify(partnership.to_dict()), 200
    else:
        return jsonify({'error':'Partnership not found'})
    
# create a partnership
@partnershipBlueprint.route('/partnerships', methods=['POST'])
def create_partnership():
    data = request.get_json()
    new_partnership = Partnership(
        user_id=data['user_id'],
        partner_name=data['partner_name'],
        description=data.get('description'),
        role=data.get('role')
    )
    
    db.session.add(new_partnership)
    db.session.commit()

    return jsonify(new_partnership.to_dict()), 201

# partial update a partnership
@partnershipBlueprint.route('/partnerships/<int:id>', methods=['PATCH'])
def patch_partnership(id):
    data = request.get_json()
    partnership = Partnership.query.get_or_404(id)

    if 'partner_name' in data:
        partnership.partner_name = data['partner_name']
    if 'description' in data:
        partnership.description = data['description']
    if 'role' in data:
        partnership.role = data['role']
    
    db.session.commit()

    return jsonify(partnership.to_dict()), 200
# full update
@partnershipBlueprint.route('/partnerships/<int:id>', methods=['PUT'])
def update_partnership(id):
    data = request.get_json()
    partnership = Partnership.query.get_or_404(id)

    partnership.user_id = data['user_id']
    partnership.partner_name = data['partner_name']
    partnership.description = data.get('description')
    partnership.role = data.get('role')
    
    db.session.commit()

    return jsonify(partnership.to_dict()), 200

@partnershipBlueprint.route('/partnerships/<int:id>', methods=['DELETE'])
def delete_partnership(id):
    partnership = Partnership.query.get_or_404(id)

    db.session.delete(partnership)
    db.session.commit()

    return jsonify({'message': 'Partnership deleted successfully'}), 204



