from functools import wraps

import jwt
from flask import request

from flaskr import config
from flaskr.model import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing!'}, 401

        try:
            data = jwt.decode(token, config.secret_key, algorithms=['HS256'])
            current_user = User.query.filter_by(publicId=data['publicId']).first()
            if not current_user:
                return {'message': 'could not find user'}, 404
        except:
            return {'message': 'Token is invalid!'}, 401

        return f(current_user, *args, **kwargs)

    return decorated
