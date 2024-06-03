from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPTokenAuth
import os
import jwt
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)
auth = HTTPTokenAuth(scheme='Bearer')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'must include username and password'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'username already taken'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'error': 'invalid credentials'}), 401
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, os.getenv('SECRET_KEY'), algorithm='HS256')
    return jsonify({'token': token}), 200

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        user = User.query.get(data['user_id'])
        return user
    except:
        return None
