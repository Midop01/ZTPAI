from flask import request, jsonify
from models.user import User
from app import db
from . import api
import jwt
from datetime import datetime, timedelta
from config import Config

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not (username and email and password):
        return jsonify({'error': 'Missing data'}), 400
    # Unique validation and error handling omitted for simplicity.
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1),
            "sub": username
        }, Config.SECRET_KEY, algorithm='HS256')
        return jsonify({
            'token': token,
            "username": username,
            "user_id": user.id
        })
    return jsonify({'error': 'Invalid credentials'}), 401
