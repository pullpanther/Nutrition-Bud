from flask import Blueprint, jsonify, request

from flaskr.extensions import db
from flaskr.model import Meal
from flaskr.schema import MealSchema

meal_bp = Blueprint('meal_bp', __name__)

schema = MealSchema()
schemas = MealSchema(many=True)


@meal_bp.route('')
def get_all_meals():
    result = Meal.query.all()
    json = jsonify(schemas.dump(result))
    return json


@meal_bp.route('/<meal_id>')
def get_meal_by_id(meal_id):
    result = Meal.query.filter_by(publicId=meal_id).first()
    json = jsonify(schema.dump(result))
    return json


@meal_bp.route('', methods=['POST'])
def create_meal():
    data = request.json

    try:
        meal = schema.load(data, session=db.session)
    except:
        print('you are missing some fields buddy')
        return jsonify({'exception': 'missing fields'})

    if Meal.query.filter_by(publicId=meal.publicId).first():
        return jsonify({'message': 'meal with that id already exists'})

    db.session.add(meal)
    db.session.commit()
    return jsonify({'message': 'successfully created meal'})


