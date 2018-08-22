import unittest
import json
from app import app, app_config
from app.api.models.questions import qtns_list
from app.api.models.user import User, users_list, user_id


class BaseTestCase(unittest.TestCase):

    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)

    def tearDown(self):
        """
        Method to tidy up lists after the test is run
        """
        users_list[:] = []
        qtns_list[:] = []

    def register_user(self, username, email, password):
        """
        Method for registering a user
        """
        return self.client.post(
            'api/v1/users/signup',
            data=json.dumps(dict(
                username=username,
                email=email,
                password=password
            )
            ),
            content_type='application/json'
        )

    def post_question(self, token, user_id, title, subject, qtn_desc):
        """
        Method for posting a question
        """
        return self.client.post(
            'api/v1/questions',
            data=json.dumps(dict(
                user_id=1,
                title=title,
                subject=subject,
                qtn_desc=qtn_desc
            )
            ),
            content_type='application/json',
            headers=({"token": token})
        )
    
    def update_question(self, token, user_id, qtn_id, title, subject, qtn_desc):
        """
        Method for updating a question
        """
        return self.client.put(
            'api/v1/questions/1',
            data=json.dumps(dict(
                qtn_id=1,
                user_id=1,
                title=title,
                subject=subject,
                qtn_desc=qtn_desc
            )
            ),
            content_type='application/json',
            headers=({"token": token})
        )
    
    def delete_question(self, token, user_id, qtn_id):
        """
        Method for deleting a question
        """
        return self.client.delete('api/v1/question/1', headers=({"token": token}))


    def login_user(self, email, password):
        """
        Method for logging a user with dummy data
        """
        return self.client.post(
            'api/v1/users/login',
            data=json.dumps({
                "email": email,
                "password": password}
            ),
            content_type='application/json'
        )
    
    def get_token(self):
        """Returns user token"""
        self.register_user("sue", "sue@gmail.com", "Bootcamp11")
        response = self.login_user("sue@gmail.com", "Bootcamp11")
        data = json.loads(response.data.decode())
        return data['token']
    
    def get_all_questions(self, token):
        """
            Method for retrieving all questions
        """
        return self.client.get('api/v1/questions', headers=({"token": token}))
    
    def get_one_question(self, token):
        """
            Method for retrieving one question from the list
        """
        return self.client.get('api/v1/question/1', headers=({"token": token}))
    
    def delete_all_questions(self, token):
        """
            Method for deleting all questions
        """
        return self.client.delete('api/v1/questions', headers=({"token": token}))

    
    def post_reply(self, token, user_id, qtn_id, reply_desc):
        """
            Method for posting reply for a question
        """
        return self.client.post(
            'api/v1/answer/1',
            data=json.dumps(dict(
                reply_desc = reply_desc,
                qtn_id = qtn_id,
                user_id = user_id

            )
            ),
            content_type='application/json',
            headers=({"token": token})
        )
    
    def delete_reply(self, token, user_id, qtn_id, reply_id):
        """Method for delete reply"""
        return self.client.delete('api/v1/answer/1/1', headers=({"token": token}))

    def delete_all_replies(self, token, user_id, qtn_id):
        """Method to delete all replies"""
        return self.client.delete('api/v1/answers/1', headers=({"token": token}))
    
    def get_all_replies(self, token, qtn_id):
        """Method to retrieve all replies"""
        return self.client.get('api/v1/answer/1', headers=({"token": token}))
    
    def get_one_reply(self, token, qtn_id, reply_id):
        """Method for retrieving one reply"""
        return self.client.get('api/v1/answer/1/1', headers=({"token": token}))

    def delete_question_with_no_token(self, token, user_id, qtn_id):
        """
        Method for deleting a question
        """
        return self.client.delete('api/v1/question/1')
