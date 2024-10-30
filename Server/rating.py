from flask import Blueprint, request, jsonify
from models import Rating, db

ratingBlueprint = Blueprint('rating', __name__)

@ratingBlueprint.route('/rating', methods=['GET'])
def get_rating():
    ratings = Rating.query.all()
    return jsonify([rating.to_dict() for rating in ratings])


@ratingBlueprint.route('/rating/<int:rating_id>', methods=['GET'])
def get_rating_by_id(rating_id):
    rating = Rating.query.get(rating_id)
    if rating is None:
        return jsonify({"message": "Rating not found"}), 404
    return jsonify(rating.to_dict()), 200


@ratingBlueprint.route('/rating', methods=['POST'])
def create_rating():
    data = request.get_json()
    new_rating = Rating(
        value=data['value'],
        user_id=data['user_id'],
        event_id=data['event_id']
    )
    db.session.add(new_rating)
    db.session.commit()
    return jsonify(new_rating.to_dict()), 201


@ratingBlueprint.route('/rating/<int:rating_id>', methods=['PUT'])
def update_rating(rating_id):
    data = request.get_json()
    rating = Rating.query.get_or_404(rating_id)
    rating.value = data['value']
    rating.user_id = data['user_id']
    rating.event_id = data['event_id']
    db.session.commit()
    return jsonify(rating.to_dict()), 200

@ratingBlueprint.route('/rating/<int:rating_id>', methods=['PATCH'])
def patch_rating(rating_id):
    data = request.get_json()
    rating = Rating.query.get_or_404(rating_id)

    if 'value' in data:
        rating.value = data['value']
    if 'user_id' in data:
        rating.user_id = data['user_id']
    if 'event_id' in data:
        rating.event_id = data['event_id']

    db.session.commit()
    return jsonify(rating.to_dict()), 200



@ratingBlueprint.route('/rating/<int:rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    rating = Rating.query.get_or_404(rating_id)
    db.session.delete(rating)
    db.session.commit()
    return jsonify({"message": "Rating deleted successfully!"}), 204

