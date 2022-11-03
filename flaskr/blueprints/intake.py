from datetime import datetime, timedelta
from operator import and_
from flask import Blueprint, jsonify, request

from flaskr.auth import token_required
from flaskr.extensions import db
from flaskr.model import Intake
from flaskr.schema import IntakeSchema

intake_bp = Blueprint('intake_bp', __name__, url_prefix='/intakes')

schema = IntakeSchema()
schemas = IntakeSchema(many=True)


@intake_bp.route('')
@token_required
def get_all_intakes(current_user):
    return jsonify(get_all_intakes_of_user(current_user)), 200


@intake_bp.route('/today')
@token_required
def get_all_intakes_today(current_user):
    return jsonify(get_intakes_of_user_today(current_user)), 200


@intake_bp.route('/macros/today')
@token_required
def get_macros_today(current_user):
    intakes = get_intakes_of_user_today(current_user)
    return get_macros_of_intakes(intakes), 200


@intake_bp.route('/macros')
@token_required
def get_macros(current_user):

    print(current_user)

    intakes = get_intakes_of_user_last_30_days(current_user)
    if not intakes:
        return jsonify([])

    grouped_intakes = group_intakes_by_date(intakes)

    macro_list = []

    for intake_group in grouped_intakes:
        macros = get_macros_of_intakes(intake_group)
        macros['date'] = intake_group[0]['date']
        macro_list.append(macros)

    return jsonify(macro_list)


@intake_bp.route('', methods=['POST'])
@token_required
def create_intake(current_user):
    data = request.json

    try:
        intake = Intake(userId=current_user.id, mealId=data['mealId'], portionSize=data['portionSize'])
    except:
        return jsonify({'exception': 'missing fields'}), 402

    db.session.add(intake)
    db.session.commit()
    return jsonify({'message': 'added intake'}), 201


@intake_bp.route('/today/<intake_id>', methods=['DELETE'])
@token_required
def delete_intake(current_user, intake_id):
    intake = Intake.query.filter(and_(
        Intake.id == intake_id,
        Intake.userId == current_user.id
    )).first()

    if not intake:
        return jsonify({'message': 'could not find intake'}), 404

    db.session.delete(intake)
    db.session.commit()

    return jsonify({'message': 'successfully deleted intake'}), 200


# Helper methods

def get_all_intakes_of_user(current_user):
    result = Intake.query.filter_by(
        userId=current_user.id
    ).all()
    return schemas.dump(result)


def get_intakes_of_user_last_30_days(current_user):
    result = Intake.query.filter(and_(
        Intake.userId == current_user.id,
        Intake.date > (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    )).all()
    return schemas.dump(result)


def get_intakes_of_user_today(current_user):
    result = Intake.query.filter(and_(
        Intake.date == date_today(),
        Intake.userId == current_user.id
    )).all()
    return schemas.dump(result)


def get_macros_of_intakes(intakes):
    result = {'totalCalories': 0, 'totalProtein': 0, 'totalFat': 0, 'totalCarbohydrates': 0}

    for intake in intakes:
        result['totalCalories'] += intake['meal']['calories'] * intake['portionSize']
        result['totalProtein'] += intake['meal']['protein'] * intake['portionSize']
        result['totalFat'] += intake['meal']['fat'] * intake['portionSize']
        result['totalCarbohydrates'] += intake['meal']['carbohydrates'] * intake['portionSize']
    return result


def group_intakes_by_date(intakes):
    intakes.sort(key=lambda x: x['date'].split('-')[::-1])

    list = [[intakes[0]]]

    i = 0
    for intake in intakes[1:]:
        if intake['date'] == list[i][0]['date']:
            list[i].append(intake)
        else:
            i += 1
            list.append([])
            list[i].append(intake)

    return list


def date_today():
    return datetime.today().strftime('%Y-%m-%d')
