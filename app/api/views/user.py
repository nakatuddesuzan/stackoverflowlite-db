from flask import Blueprint, request, jsonify, make_response
from app.api.models.user import User, users_list
from app import generate_id


auth = Blueprint('auth', __name__)

@auth.route('/api/v1/users/signup', methods=['POST'])
def register_user():
    if not request.get_json():
        return make_response(jsonify({"message": "Request should be json"}), 400)
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    user_id = generate_id(users_list)
    user = {
            'username' : username,
            'email': email,
            'password': password,
            'user_id': user_id
    } 
    
    User('user_id', username=username, email=email, password=password)
   
    for user in users_list:
        if email == user["email"] and username == user["username"]:
            return make_response(jsonify({'message': 'User already exists'}))
        elif email == user["email"]:
            return make_response(jsonify({'message': 'Email already in use'}))
    users_list.append(user)

    return jsonify(user), 201

@auth.route('/api/v1/users/login', methods=['POST'])
def login_user():
    """ Allows users to log into their accounts"""
    if not request.get_json():
        return make_response(jsonify({"message": "Request should be json"}), 400)

    email = request.get_json()['email']
    password = request.get_json()['password']

    for user in users_list:
        if email == user['email'] and password == user['password']:
            access_token = "{}".format(
                User.encode_auth_token(user['user_id']))
            return make_response(jsonify({
                "token": access_token,
                "message": "Login successful"
                }), 200)
    return make_response(jsonify({
        "message": "wrong username or password"}), 401)
