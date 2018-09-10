import logging
from functools import wraps
from app.api.models.user import User
from app.api.db_manager.db_config import DatabaseConnection

import jwt
from flask import request, jsonify, make_response,g


def login_required(func):
    """
    login_required. protects a route to only authenticated users
    """
    @wraps(func)
    def auth(*args, **kwargs):
        try:
            access_token = request.headers.get('token', '')
            if access_token.strip(' '):
                decoded = User.decode_auth_token(access_token)
                print(decoded)
                if decoded["status"]:
                    return func(*args, **kwargs)
                return make_response(jsonify({"message": "Invalid token.Please login"}))
            return make_response(jsonify({ "message": "Token missing. Provide token"}))
        except Exception as e:
            logging.error(e)
            return make_response(jsonify({'message': str(e)}), 500)
    return auth
    