import os

db_path = os.path.join(os.path.dirname(__file__), 'flaskr/data/database.db')
db_uri = 'sqlite:///{}'.format(db_path)
SQLALCHEMY_DATABASE_URI = db_uri
secret_key = 'SECRET_KEY'
