import json
from tests.base import BaseTestCase
from app.api.models.user import User, users_list, user_id

class TestUserAuth(BaseTestCase):


    def test_if_user_class_exists(self):
        user = User(1,"sue", "sue@gmail.com", "Bootcamp11")
        self.assertTrue(user)

    def test_if_json_data(self):
        """
            Test for json data
        """
        with self.client:
            response = self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            self.assertTrue(response.content_type == 'application/json')

    def test_json_data_error_response(self):
        """
            Test error message if not json data provided
        """
        response = self.register_user("sue", "sue@gmail.com", "Bootcamp11")
        data = json.loads(response.data.decode())
        self.assertNotEqual(data.get('message'), "Request should be json")

    def test_json_data_error_response_code(self):
        """
            Test response code if not json data provided
        """
        response = self.register_user("sue", "sue@gmail.com", "Bootcamp11")
        self.assertNotEqual(response.status_code, 400)

    def test_successful_signup(self):
        """
            Test for successful user signup
        """
        with self.client:
            response = self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            self.assertEqual(response.status_code, 201)

    def test_signup_with_esisting_email(self):
        """
            Tests if User is Registering with an already used email
        """
        with self.client:
            self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            response = self.register_user("boolean", "sue@gmail.com", "bootcamp12")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Email already in use")
            
    def test_existing_user(self):
        """
            Tests for no duplicate user
        """
        with self.client:
            self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            response = self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "User already exists")

    def test_valid_email(self):
        """
            Test for valid email entry
        """
        with self.client:
            self.assertRaises(
                ValueError, lambda: self.register_user("sue", "suegmail.com", "Bootcamp11")
            )
    def test_empty_email_field(self):
        """
            Test for empty email field
        """
        with self.client:
            self.assertRaises(
                Exception, lambda: self.register_user("sue", "", "Bootcamp11")
            )
    def test_invalid_password(self):
        """
            Test for invalid password
        """
        with self.client:
            self.assertRaises(
                Exception, lambda: self.register_user("sue", "sue@gmail.com", 123456789)
            )
    
    def test_password_length(self):
        """
            Test for password length < 8 characters
        """
        with self.client:
            self.assertRaises(
                Exception, lambda: self.register_user("sue", "sue@gmail.com", "Boo")
            )
    
    def test_if_passsword_has_only_characters(self):
        """
            Test for password has characters only
        """
        with self.client:
            self.assertRaises(
                Exception, lambda: self.register_user("sue", "sue@gmail.com", "Bootcampers")
            )
    
    def test_empty_password_field(self):
        """
            Test for password not provided
        """
        with self.client:
            self.assertRaises(
                Exception, lambda: self.register_user("sue", "sue@gmail.com", "")
            )
    
    def test_invalid_user_name_length(self):
        """
            Test for invalid name length
        """
        with self.client:
            self.assertRaises(
                Exception, lambda: self.register_user("su", "sue@gmail.com", "Bootcamp11")
            )
    
    def test_invalid_name(self):
        """
            Test for invalid characters 
            in the neme after compilation
        """
        with self.client:
            self.assertRaises(
                ValueError, lambda: self.register_user("!@#", "sue@gmail.com", "Bootcamp11")
            )

    def test_empty_user_name_field(self):
        """
            Test for empty username field
        """
        with self.client:
            self.assertRaises(
                Exception, lambda: self.register_user("", "sue@gmail.com", "Bootcamp11")
            )
    def test_status_code_on_succesful_login(self):
        with self.client:
            self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            response = self.login_user("sue@gmail.com", "Bootcamp11")
            self.assertEqual(response.status_code, 200)

    def test_message_on_succesful_login(self):
        with self.client:
            self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            response = self.login_user("sue@gmail.com", "Bootcamp11")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Login successful")
    
    def test_login_using_wrong_credentials(self):

        with self.client:
            self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            response = self.login_user("peter@gmail.com", "Bootcamp12")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "wrong username or password")
    
    def test_if_encode_auth_token(self):
        with self.client:
            user = User(1,"sue", "sue@gmail.com", "Bootcamp11")
            users_list.append(user)
            auth_token = user.encode_auth_token(user_id)
            self.assertFalse(isinstance(auth_token, bytes))
            
    def test_if_user_gets_token_on_log_in(self):
        """Test for user login token"""
        with self.client:
            self.register_user("sue", "sue@gmail.com", "Bootcamp11")
            response = self.login_user("sue@gmail.com", "Bootcamp11")
            data = json.loads(response.data.decode())
            self.assertTrue(data['token'])
