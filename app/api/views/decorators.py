import logging
from functools import wraps
from app.api.models.user import User
from app.api.db_manager.db_config import DatabaseConnection

import jwt
from flask import request, jsonify, make_response


def login_required(func):
    """
    login_required. protects a route to only authenticated users
    """
    @wraps(func)
    def auth(*args, **kwargs):
        try:
            with DatabaseConnection() as cursor:
                access_token = request.headers['Authorization']
                token = access_token
                if token is None:
                    return jsonify({"message": "No token, please provide a token"}), 401
                if token:
                    user_id = User.decode_auth_token(token)[0]
                    cursor.execute("SELECT * FROM users WHERE user_id = '%s'" % user_id)
                    user_fetched= cursor.fetchone()
                    user_instance = list(user_fetched)
                    user = User(*user_instance)
                    if user:
                        return func(user, *args,**kwargs)
                    return jsonify({'message': user_id}),401
            
        except Exception as e:
            raise e
    return auth
    