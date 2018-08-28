import logging
import jwt
from flask import json
from datetime import datetime, timedelta
from flasgger.utils import swag_from
from app.config import app_config
from app import app as current_app

from flask import Blueprint, request, jsonify, make_response
from app.api.models.user import User
from app.api.db_manager.db_config import DatabaseConnection


auth = Blueprint('auth', __name__) 

@swag_from('../apidocs/signup.yml')
@auth.route('/api/v1/users/signup', methods=['POST'])
def register_user():
    try:
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']
        user = User('user_id', username=username, email=email, password=password)
        new_user = User.insert_user_data(user)
        print(new_user)
        return new_user
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)


@auth.route('/api/v1/users/login', methods=['POST'])
def login_user():
    """ Allows users to log into their accounts"""
    try:
        with DatabaseConnection() as cursor:
            if not request.get_json():
                return make_response(jsonify({"message": "Request should be json"}), 400)
            email = request.get_json()['email']
            password = request.get_json()['password']
            sql = "select user_id, email, password from users where email = %s and password = %s"
            cursor.execute(sql, (email, password))
            user_id = cursor.fetchone()
            if user_id:
                payload = {
                #expiration date of the token
                'exp': datetime.utcnow() + timedelta(minutes=30),
                # international atomic time
                #the time the token is generated
                'iat': datetime.utcnow(),
                # the subject of the token 
                # (the user whom it identifies)
                "email": email[1]
                }

                token = jwt.encode(
                    payload,
                    current_app.config.get('SECRET_KEY'),
                    algorithm= 'HS256'
                ).decode('UTF-8')

                if token:
                    response = {
                        'user_id': user_id[0],
                        'message': 'You logged in successfully',
                        'token': token,
                        'email': email
                    }
                return make_response(jsonify(response)), 200
            else:
                return make_response(jsonify({"message": "wrong password or email credentials"}))

    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 401)
