import logging
from functools import wraps

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
        try:
            data = jwt.decode(access_token, 'secret', verify=False)
        except Exception as e:
            logging.error(e)
            return make_response(jsonify({"message": "Invalid Token"}), 400)
        return func(data["user_id"], *args, **kwargs)
        
    return auth
