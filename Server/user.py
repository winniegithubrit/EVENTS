from flask import Blueprint, request,jsonify
from models import User,db
import firebase_admin.auth as auth

userBlueprint = Blueprint('user', __name__)
@userBlueprint.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list), 200

# get user by id
@userBlueprint.route('/users/<int:user_id>', methods=['GET'])
def get_users_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error':'User not found'}), 404

# AUTHENTICATING USERS 
@userBlueprint.route('/register', methods=['POST'])
def register_user():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        new_user = User(username=username, email=email, password=password) 
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User has been created successfully', 'user_id': user.uid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# login user
@userBlueprint.route('/login', methods=['POST'])
def login_user():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = auth.get_user_by_email(email)
        id_token = auth.create_custom_token(user.uid)
        return jsonify({'message': 'User has been logged in successfully', 'token': id_token.decode('utf-8')}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401


    
def verify_token(token):
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid'] 
    except Exception as e:
        print(f"Token verification error: {str(e)}")  
        return None

# protected route to detect the routes
@userBlueprint.route('/protected', methods=['GET'])
def protected_route():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'error': 'Authorization header is missing'}), 401

    # Check if the header starts with "Bearer"
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid authorization header format'}), 401

    # Extract the token
    token = auth_header.split(' ')[1]
    
    # Verify the token
    user_id = verify_token(token)

    if user_id:
        return jsonify({'message': 'You are authenticated!', 'user_id': user_id}), 200
    else:
        return jsonify({'error': 'Unauthorized, token may be invalid'}), 401


