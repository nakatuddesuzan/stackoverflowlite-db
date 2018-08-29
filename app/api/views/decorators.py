import logging
from functools import wraps
from app.api.models.user import User

import jwt
from flask import request, jsonify, make_response


def login_required(func):
    """
    login_required. protects a route to only authenticated users
    """
    @wraps(func)
    def auth(*args, **kwargs):
        access_token = request.headers.get('token')
        if access_token is None:
            return jsonify({"message": "No token, please provide a token"}), 401
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                return func(user_id,*args,**kwargs)
            return jsonify({'message': user_id}),401
    return auth
