import logging

from flask import Blueprint, request, jsonify, make_response
from app.api.models.user import User
from flask import json
# from app.api.db_manager.db_config import Database


auth = Blueprint('auth', __name__)

@auth.route('/api/v1/users/signup', methods=['POST'])
def register_user():
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']
        user = User('user_id', username=username, email=email, password=password)
        
        new_user = User.insert_user_data(user)
        return make_response(jsonify({"message": new_user["message"]}),  new_user["status"])

    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)


@auth.route('/api/v1/users/login', methods=['POST'])
def login_user():
    """ Allows users to log into their accounts"""
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)

        email = request.get_json()['email']
        password = request.get_json()['password']
        
        user_login = User.log_in_user(email, password)
        
        
        return make_response(jsonify(user_login), 200)

    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 401)
