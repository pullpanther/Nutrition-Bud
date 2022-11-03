from flaskr.extensions import ma
from flaskr.model import Meal, User, Intake, Goal


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    publicId = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()


class MealSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Meal
        load_instance = True

    id = ma.auto_field()
    publicId = ma.auto_field()
    name = ma.auto_field()
    portion = ma.auto_field()
    portionType = ma.auto_field()
    calories = ma.auto_field()
    fat = ma.auto_field()
    carbohydrates = ma.auto_field()
    protein = ma.auto_field()


class IntakeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Intake
        load_instance = True

    portionSize = ma.auto_field()
    meal = ma.Nested(MealSchema)
    id = ma.auto_field()
    date = ma.auto_field()
    time = ma.auto_field()
    userId = ma.auto_field()


class GoalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Goal
        load_instance = True

    calories = ma.auto_field()
    fat = ma.auto_field()
    protein = ma.auto_field()
    carbohydrates = ma.auto_field()


