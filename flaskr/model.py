import datetime

from flaskr.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    portion = db.Column(db.Integer, nullable=False)
    portionType = db.Column(db.String(4), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)


class Intake(db.Model):
    portionSize = db.Column(db.Float(), nullable=False)
    mealId = db.Column(db.String, db.ForeignKey('meal.publicId'), nullable=False)

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String(20), default=datetime.datetime.now().strftime('%Y-%m-%d'), nullable=False)
    time = db.Column(db.String(20), default=datetime.datetime.now().strftime('%R'), nullable=False)
    userId = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship(User, backref='user_intakes')
    meal = db.relationship(Meal, backref='meal_intakes')


class Goal(db.Model):
    userId = db.Column(db.String, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    user = db.relationship(User, backref='user_goals')

    calories = db.Column(db.Float())
    fat = db.Column(db.Float())
    protein = db.Column(db.Float())
    carbohydrates = db.Column(db.Float())

