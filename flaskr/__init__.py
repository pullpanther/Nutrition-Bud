import os

from flask import Flask
# from flask_restful import Api

from flaskr.blueprints.intake import intake_bp
from flaskr.blueprints.meal import meal_bp
from flaskr.blueprints.user import user_bp
from flaskr.extensions import db, ma


def create_app():
    app = Flask(__name__)

    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)
    ma.init_app(app)

    BASE = '/api/v1'

    app.register_blueprint(intake_bp, url_prefix=BASE + '/intakes')
    app.register_blueprint(user_bp, url_prefix=BASE + '/users')
    app.register_blueprint(meal_bp, url_prefix=BASE + '/meals')

    return app
