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

        access_token = request.headers.get('token', '')
        if not access_token:
            return jsonify({"message": "No token, please provide a token"}), 401
        try:
            with DatabaseConnection() as cursor: 
                response = User.decode_auth_token(access_token)
                cursor.execute("SELECT * FROM users WHERE user_id = '%s'" % response)
                user_fetched= cursor.fetchone()
                user_instance = list(user_fetched)
                user = User(*user_instance)
                return func(user, *args,**kwargs)
                        
        except:
            return jsonify({'message': response}),401
            
    return auth
    