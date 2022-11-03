import datetime
import uuid

import jwt
from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr import config
from flaskr.auth import token_required
from flaskr.extensions import db
from flaskr.model import User, Goal
from flaskr.schema import UserSchema, GoalSchema

user_bp = Blueprint('user_bp', __name__)

userSchema = UserSchema()
userSchemas = UserSchema(many=True)
goalSchema = GoalSchema()


def message(mess):
    return jsonify({'message': mess})


@user_bp.route('', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return message('access denied')

    result = User.query.all()
    json = jsonify(userSchemas.dump(result))
    return json, 200


@user_bp.route('/<public_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, public_id):
    if not current_user.admin:
        return message('access denied')

    result = User.query.filter_by(publicId=public_id).first()
    json = jsonify(userSchema.dump(result))
    return json


@user_bp.route('', methods=['POST'])
def create_user():
    data = request.json

    if not data['email']:
        return message('Email missing'), 401
    if not data['password']:
        return message('Password missing'), 401
    if not data['firstName']:
        return message('first name missing'), 401
    if not data['lastName']:
        return message('last name missing'), 401

    if User.query.filter_by(email=data['email']).first():
        return message('email already exists'), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(publicId=str(uuid.uuid4()), email=data['email'], password=hashed_password, admin=False)
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return message('Something went wrong'), 422

    return message('New user created'), 201


@user_bp.route('/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return message('access denied')

    user = User.query.filter_by(publicId=public_id).first()
    if not user:
        return message('No user found')

    user.admin = True

    try:
        db.session.commit()
    except:
        return message('Something went wrong'), 422
    return message('user has been promoted')


@user_bp.route('/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return message('access denied')

    user = User.query.filter_by(publicId=public_id).first()
    if not user:
        return message('No user found')

    db.session.delete(user)

    try:
        db.session.commit()
    except:
        return message('Something went wrong'), 422

    return message('user has been deleted')


@user_bp.route('/login', methods=['GET'])
def login():
    auth = request.authorization

    if not auth:
        return jsonify({'message': 'No Authentication'}), 401
    if not auth.username:
        return jsonify({'message': 'Email missing'}), 401
    if not auth.password:
        return jsonify({'message': 'Password missing'}), 401

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return jsonify({'message': 'Could not find user with that email'}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'publicId': user.publicId, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            config.secret_key)
        return {'token': token}

    return jsonify({'message': 'Wrong email/password combination'}), 401


@user_bp.route('/login/verify', methods=['GET'])
@token_required
def verify_token(current_user):
    return message('verified'), 200


@user_bp.route('/goals', methods=['GET'])
@token_required
def get_user_goals(current_user):
    result = Goal.query.filter_by(userId=current_user.id).first()
    return jsonify(goalSchema.dump(result)), 200


@user_bp.route('/goals', methods=['POST'])
@token_required
def create_user_goals(current_user):
    data = request.json
    goal = goalSchema.load(data, session=db.session)
    goal.userId = current_user.id
    db.session.add(goal)

    try:
        db.session.commit()
    except:
        return message('Something went wrong'), 422

    return message('Goals successfully added'), 201


@user_bp.route('/goals', methods=['PUT'])
@token_required
def update_user_goals(current_user):
    data = request.json
    goal = Goal.query.filter_by(userId=current_user.id).first()

    if data.get('calories'):
        goal.calories = data['calories']
    if data.get('protein'):
        goal.protein = data['protein']
    if data.get('fat'):
        goal.fat = data['fat']
    if data.get('carbohydrates'):
        goal.carbohydrates = data['carbohydrates']

    try:
        db.session.commit()
    except:
        return message('Something went wrong'), 422

    return message('Updated goals successfully'), 200
