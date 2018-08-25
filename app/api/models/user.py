from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import re
from flask import jsonify, make_response
from app import generate_id
from flask import current_app, g
from app.api.db_manager.db_config import DatabaseConnection


class User(DatabaseConnection):
    """Class representing User model"""

    def __init__(self, user_id, username, email, password):
        DatabaseConnection.__init__(self)
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.signed_in = 0

    @property
    def password(self): 
        return self._password   # pragma: no cover

    @password.setter
    def password(self, pwd):
        if not pwd:
            raise Exception("Field can't be empty")
        if len(pwd) < 8 or len(pwd) > 12:
            raise Exception(
                "Weak password \n Password must be 8 characters long ")
        if not re.search(r'[0-9]', pwd):
            raise Exception(
                'Weak password \n Password should have atleast one integer')
        if pwd.isupper() or pwd.islower() or pwd.isdigit():
            print("Weak password")
        self._password = pwd

    @property
    def email(self):
        return self._email  # pragma: no cover

    @email.setter
    def email(self, value):
        if not value:
            raise Exception("Email field can't be empty")
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", value):
            raise ValueError('Enter Valid Email ID forexample "sue@gmail.com"')
        self._email = value

    @property
    def username(self):
        return self._username   # pragma: no cover

    @username.setter
    def username(self, value):
        if not value:
            raise Exception("Field can't be empty")
        if len(value) <= 2:
            raise Exception("Name too sort \n  Not allowed")
        if re.compile('[!@#$%^&*:;?><.0-9]').match(value):
            raise ValueError("Invalid characters not allowed")

        self._username = value
    
    def create_user_table(self):  
        sql = "CREATE TABLE IF NOT EXISTs users( user_id SERIAL PRIMARY KEY, username VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(12) NOT NULL)"
        self.cursor.execute(sql)
    
    def insert_user_data(self):
        sql = "INSERT INTO  users(username, email, password) VALUES(%s, %s, %s) "
        try:
            self.cursor.execute("SELECT * FROM users WHERE email = '%s'" % self.email)

            if self.cursor.fetchone():
                    return {"message": "Email already in use", "status":400}
            else:
                self.cursor.execute(sql, (self.username, self.email, self.password))
                self.cursor.execute(
                        "SELECT * FROM users WHERE email = '%s'" % self.email)
                self.conn.commit()
                result_user = self.cursor.fetchone()
                return {"message":self.user_dict(result_user),
                    "status":201}
        except Exception as e:
            return e
    
    @staticmethod
    def user_dict(user):
        return {
            "user_id": user[0],
            "username": user[1],
            "email": user[2],
            "password": user[3]
        }

    @staticmethod
    def log_in_user(email, password):
        try:
            with DatabaseConnection() as cursor:
                sql = "select id,email, password from users where email = %s and password = %s"
                logged_in = "update users set logged_in = TRUE where email = %s and password = %s"

                cursor.execute(sql, (email, password))
                user = cursor.fetchone()
                if user:
                    token = jwt.encode(
                        {'email': email, 'user_id': user[0]}, 'secret', algorithm='HS256')
                if token:
                    response = {
                        'message': 'You logged in successfully.',
                        'token': token.decode('UTF-8'),
                        'email': user.email,
                        'username': user.username,
                        'Id': user.id
                    }
                    cursor.execute(logged_in, (email, password))
                    return make_response(jsonify(response)), 200

        except Exception as e:
            return e

    # @staticmethod
    # def encode_auth_token(user_id):
    #     """
    #     Generates the Auth Token
    #     :return: string
    #     """
    #     try:
    #         """ set payload expiration time"""
    #         payload = {
    #             #expiration date of the token
    #             'exp': datetime.utcnow() + timedelta(minutes=30),
    #             # international atomic time
    #             #the time the token is generated
    #             'iat': datetime.utcnow(),
    #             # the subject of the token 
    #             # (the user whom it identifies)
    #             'sub': user_id
                
    #         }
    #         return jwt.encode(
    #             payload,
    #             current_app.config.get('SECRET_KEY'),
    #             algorithm='HS256'
    #         ).decode('UTF-8')
            
    #     except Exception as e:
    #         return e

    # @staticmethod
    # def decode_auth_token(auth_token):
    #     """
    #     Decodes the auth token
    #     :param auth_token:
    #     :return: integer|string
    #     """
    #     try:
    #         payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
    #         user = {'user_id': payload['sub'],
    #                 'status': 'Success'
    #         }
    #         #add user to context
    #         g.user = user
    #         return user
    #     except jwt.ExpiredSignatureError:
    #         return 'Signature expired. Please log in again.'
    #     except jwt.InvalidTokenError:
    #         return 'Invalid token. Please log in again.'