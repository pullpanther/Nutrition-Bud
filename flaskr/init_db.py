import uuid

from werkzeug.security import generate_password_hash

from flaskr.extensions import db

from flaskr import create_app
from flaskr.model import User, Meal, Intake, Goal

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    userId = str(uuid.uuid4())

    user1 = User(publicId=userId, email='example.email@gmail.com',
                 password=generate_password_hash('12345', method='sha256'), admin=True, firstName='firstname',
                 lastName='lastname')

    db.session.add_all([user1])

    meal1 = Meal(publicId='8710624233334', name='Lactose vrije melk halfvol', portion=100, portionType='ml',
                 calories=46, fat=1, protein=3, carbohydrates=4)
    meal2 = Meal(publicId='4008404001001', name='Knusperbrot', portion=100, portionType='g', calories=380, fat=3,
                 protein=1, carbohydrates=72)
    meal3 = Meal(publicId='4061458020183', name='Tonijn', portion=100, portionType='g', calories=110, fat=25,
                 protein=26, carbohydrates=0.5)

    db.session.add_all([meal1, meal2, meal3])

    db.session.add(Goal(userId=1, calories=1800, protein=120,))

    db.session.add(Intake(portionSize=1, userId=1, mealId='4008404001001', date='2022-05-11'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4061458020183', date='2022-05-09'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4008404001001', date='2022-05-09'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4008404001001', date='2022-05-10'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='8710624233334', date='2022-05-10'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='8710624233334', date='2022-05-11'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4008404001001', date='2022-05-09'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4008404001001', date='2022-05-11'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='8710624233334', date='2022-05-14'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4061458020183', date='2022-05-11'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4008404001001', date='2022-05-12'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4061458020183', date='2022-05-09'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4061458020183', date='2022-05-12'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='4008404001001', date='2022-05-09'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='8710624233334', date='2022-05-13'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='8710624233334', date='2022-05-12'))
    db.session.add(Intake(portionSize=1, userId=1, mealId='8710624233334', date='2022-05-10'))

    db.session.commit()
