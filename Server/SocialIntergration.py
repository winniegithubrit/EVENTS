from flask import Blueprint, request, jsonify
from models import SocialIntergration, db

socialIntegrationBlueprint = Blueprint('socialIntegration', __name__)

@socialIntegrationBlueprint.route('/socialIntegration', methods=['GET'])
def get_social_integrations():
    social_integrations = SocialIntergration.query.all()
    return jsonify([social_integration.to_dict() for social_integration in social_integrations])


@socialIntegrationBlueprint.route('/socialIntegration<int:social_integration_id>', methods=['GET'])
def get_social_integration_by_id(social_integration_id):
    social_integration = SocialIntergration.query.get(social_integration_id)
    if social_integration is None:
        return jsonify({"message": "Social Integration not found"}), 404
    return jsonify(social_integration.to_dict()), 200


@socialIntegrationBlueprint.route('/socialIntegration', methods=['POST'])
def create_social_integration():
    data = request.get_json()
    new_social_integration = SocialIntergration(
        event_id=data['event_id'],
        user_id=data['user_id'],
        shared_with=data['shared_with']
    )
    db.session.add(new_social_integration)
    db.session.commit()
    return jsonify(new_social_integration.to_dict()), 201


@socialIntegrationBlueprint.route('/socialIntegration/<int:social_integration_id>', methods=['PATCH'])
def update_social_integration(social_integration_id):
    data = request.get_json()
    social_integration = SocialIntergration.query.get(social_integration_id)

    if 'event_id' in data:
        social_integration.event_id = data['event_id']
    if 'user_id' in data:
        social_integration.user_id = data['user_id']
    if 'shared_with' in data:
        social_integration.shared_with = data['shared_with']

    db.session.commit()
    return jsonify(social_integration.to_dict()), 200

@socialIntegrationBlueprint.route('/socialIntegration/<int:social_integration_id>', methods=['PUT'])
def update_social_integration_by_id(social_integration_id):
    data = request.get_json()
    social_integration = SocialIntergration.query.get(social_integration_id)
    social_integration.event_id = data['event_id']
    social_integration.user_id = data['user_id']
    social_integration.shared_with = data['shared_with']
    db.session.commit()
    return jsonify(social_integration.to_dict()), 200

@socialIntegrationBlueprint.route('/socialIntegration/<int:social_integration_id>', methods=['DELETE'])
def delete_social_integration(social_integration_id):
    social_integration = SocialIntergration.query.get(social_integration_id)
    if social_integration is None:
        return jsonify({"message": "Social Integration not found"}), 404
    db.session.delete(social_integration)
    db.session.commit()
    return jsonify({"message": "Social Integration deleted"}), 200

