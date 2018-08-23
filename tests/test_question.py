import json
from tests.base import BaseTestCase
from app.api.models.questions import Question


class TestQuestion(BaseTestCase):


    def test_if_questions_class_exists(self):
        question = Question(1, "flask", "python", "importing files")
        self.assertTrue(question)
        
    def test_if_json_data(self):
        """
            Test for json question data
        """
        with self.client:
            token = self.get_token()
            response = self.post_question(token,  1,"flask", "python", "importing files")
            self.assertTrue(response.content_type == 'application/json')

    def test_json_data_error_response(self):
        """
            Test error message if not json data provided
        """
        with self.client:
            token = self.get_token()
            response = self.post_question(token,  1,"flask", "python", "importing files")
            data = json.loads(response.data.decode())
            self.assertNotEqual(data.get('message'), "Request should be json")

    def test_json_data_error_response_code(self):
        """
            Test response code if not json data provided
        """
        with self.client:
            token = self.get_token()
            response = self.post_question(token,  1,"flask", "python", "importing files")
            self.assertNotEqual(response.status_code, 400)

    def test_question_added_successfully(self):
        """
            Test for successful posting of a questsion
        """
        with self.client:
            token = self.get_token()
            response = self.post_question(token,  1,"flask", "python", "importing files")
            self.assertEqual(response.status_code, 201)

    def test_auth_to_post_question(self):
        """
            Test for an 
            unathorized user can post a questsion
        """
        with self.client:
            response = self.post_question("id",  1,"flask", "python", "importing files")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),"Invalid token. Please log in again.")

    def test_get_all_questions(self):
        """test if user can retrieve all questions"""

        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.get_all_questions(token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['questions'])

    def test_retrieve_one_questions(self):
        """test if user can retrieve one question"""

        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.get_one_question(token)
            self.assertEqual(response.status_code, 200)

    def test_delete_question(self):
        """test if user can delete one question"""

        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.delete_question(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['questions'], [])
            self.assertEqual(response.status_code, 200)
    
    def test_update_question(self):
        """test if user can update a question"""

        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.update_question(token, 1, 1, "not working", "CSS", "chjushxhxbh" )
            data = json.loads(response.data.decode())
            self.assertTrue(data['Updated'])
            self.assertEqual(response.status_code, 200)

    def test_json_data_error_response_for_update_question(self):
        """
            Test error message if not json data provided
        """
        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.update_question(token, 1, 1, "not working", "CSS", "chjushxhxbh" )
            data = json.loads(response.data.decode())
            self.assertNotEqual(data.get('message'), "Request should be json")

    def test_json_data_error_response_code_for_update_question(self):
        """
            Test response code if not json data provided
        """
        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.update_question(token, 1, 1, "not working", "CSS", "chjushxhxbh" )
            self.assertNotEqual(response.status_code, 400)
    
    def test_delete_all_questions(self):
        """test if all questions can be deleted"""
        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.delete_all_questions(token)
            data = json.loads(response.data.decode())
            self.assertEqual(data['Replies left'], [])

    def test_delete_all_questions_with_empty_qtns_list(self):
        """
            Test for delete all questions for abn already empty list
        """
        with self.client:
            token = self.get_token()
            response = self.delete_all_questions(token)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'List empty')
    
    def test_update_missing_questions(self):
        """
            Test for trying to delete questions that don't exist
        """
        with self.client:
            token = self.get_token()
            response = self.update_question(token, 2, 1, "not working", "CSS", "chjushxhxbh" )
            data = json.loads(response.data.decode())
            self.assertEqual(data['Updated'], "Question not found")
    
    def test_delete_missing_question(self):
        """
            Test for trying to delete a question that doesn.t exist
        """
        with self.client:
            token = self.get_token()
            response = self.delete_question(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "No questions found")

    def test_unauthorized_deleting_question(self):
        """Tests if user can delete queetions without logging"""
        with self.client:
            token = self.get_token()
            self.post_question(token,  1, "flask", "python", "importing files")
            response = self.delete_question_with_no_token(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "No token, please provide a token")
            self.assertEqual(response.status_code, 401)
