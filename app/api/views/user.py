import logging
import jwt
from flask import json
from datetime import datetime, timedelta
from flasgger import swag_from
from app.config import app_config
from app import app as current_app

from flask import Blueprint, request, jsonify, make_response
from app.api.models.user import User
from app.api.db_manager.db_config import DatabaseConnection
from app.api.views.decorators import login_required


auth = Blueprint('auth', __name__) 

@auth.route('/api/v1/users/signup', methods=['POST'])
@swag_from("../docs/signup.yml")
def register_user():
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        username = request.get_json()['username'].strip()
        email = request.get_json()['email'].strip()
        password = request.get_json()['password'].strip()
        user = User('user_id', username=username, email=email, password=password)
        new_user = User.insert_user_data(user)
        return new_user
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@auth.route('/api/v1/users/login', methods=['POST'])
@swag_from("../docs/login.yml")
def login_user():
    """ Allows users to log into their accounts"""
    try:
        with DatabaseConnection() as cursor:
            if not request.get_json():
                return make_response(jsonify({"message": "Request should be json"}), 400)
            email = request.get_json()['email']
            password = request.get_json()['password']
            sql = "select user_id, email, username, password from users where email = %s and password = %s"
            cursor.execute(sql, (email, password))
            user_id = cursor.fetchone()
            if user_id:
                token = User.encode_auth_token(user_id)
                if token:
                    response = {
                        'user_id': user_id[0],
                        'message': 'You logged in successfully',
                        'token': token,
                        'username': user_id[2],
                        'email': email
                    }
                    return make_response(jsonify(response))
                
            else:
                return make_response(jsonify({"message": "wrong password or email credentials"}))

    except Exception as e:# pragma: no cover
        raise e # pragma: no cover


@auth.route('/api/v1/users', methods=['PUT'])
@login_required
def edit_profile(user):
    try:
        username = request.get_json()['username'].strip()
        email = request.get_json()['email'].strip()
        password = request.get_json()['password'].strip()
        new_user = User.edit_user(user.user_id, username, email, password)
        print(new_user)
        return make_response(jsonify({"message":"User updated succsefully"}, 201))
    except Exception as e:# pragma: no cover
        raise e # pragma: no cover

@auth.route('/api/v1/users/bio', methods=['PUT'])
@login_required
def add_bio(user):
    try:
        bio = request.get_json()['bio'].strip()
        print()
        User.add_bio(user.user_id, bio)
        return make_response(jsonify({"message":"Bio Updated"}), 201)
    except Exception as e:# pragma: no cover
        raise e # pragma: no cover

@auth.route('/api/v1/users/bio', methods=["GET"])
@login_required
def get_bio(user):
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT bio FROM users WHERE user_id = %s" % user.user_id)
            bio = cursor.fetchone()
            if bio:
                return make_response(jsonify(bio), 200)
            return make_response(jsonify({'message':'Please add bio to your profile'}))
    except Exception as e: # pragma: no cover
        return e # pragma: no cover 