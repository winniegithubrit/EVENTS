from flask import Blueprint, jsonify, request
from models import Review, db
from datetime import datetime

reviewBlueprint = Blueprint('review', __name__)

@reviewBlueprint.route('/review', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews])

@reviewBlueprint.route('/review/<int:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review = Review.query.get(review_id)
    if review is None:
        return jsonify({"message": "Review not found"}), 404
    return jsonify(review.to_dict()), 200


@reviewBlueprint.route('/review', methods=['POST'])
def create_review():
    data = request.get_json()
    new_review = Review(
        rating=data['rating'],
        comment=data['comment'],
        user_id=data['user_id'],
        event_id=data['event_id']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201

@reviewBlueprint.route('/review/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = Review.query.get_or_404(review_id)

    review.rating = data['rating']
    review.comment = data['comment']
    review.user_id = data['user_id']
    review.event_id = data['event_id']

    db.session.commit()
    return jsonify(review.to_dict()), 200

@reviewBlueprint.route('/review/<int:review_id>', methods=['PATCH'])
def patch_review(review_id):
    data = request.get_json()
    review = Review.query.get_or_404(review_id)

    if 'rating' in data:
        review.rating = data['rating']
    if 'comment' in data:
        review.comment = data['comment']
    if 'user_id' in data:
        review.user_id = data['user_id']
    if 'event_id' in data:
        review.event_id = data['event_id']

    db.session.commit()
    return jsonify(review.to_dict()), 200

@reviewBlueprint.route('/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review is None:
        return jsonify({"message": "Review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted successfully!"}), 204