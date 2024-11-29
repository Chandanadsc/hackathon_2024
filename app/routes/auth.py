from flask import Blueprint, request, jsonify
from app.config.database import get_async_db, hash_password, verify_password
from app.models.models import User
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')

@auth_bp.route('/signup', methods=['POST'])
async def signup():
    try:
        data = request.get_json()
        db = await get_async_db()
        
        # Check if user exists
        existing_user = await db.users.find_one({'email': data['email']})
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        hashed_password = hash_password(data['password'])
        user = User(
            email=data['email'],
            password_hash=hashed_password,
            name=data['name']
        )
        
        result = await db.users.insert_one(user.dict(by_alias=True))
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': str(result.inserted_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, JWT_SECRET)
        
        return jsonify({
            'token': token,
            'user': {
                'id': str(result.inserted_id),
                'email': user.email,
                'name': user.name
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/signin', methods=['POST'])
async def signin():
    try:
        data = request.get_json()
        db = await get_async_db()
        
        user = await db.users.find_one({'email': data['email']})
        if not user or not verify_password(data['password'], user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, JWT_SECRET)
        
        return jsonify({
            'token': token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user['name']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 