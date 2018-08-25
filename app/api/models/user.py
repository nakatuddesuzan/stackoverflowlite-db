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
