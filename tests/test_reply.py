import json

from tests.base import BaseTestCase
from app.api.models.reply import Reply


class TestReplies(BaseTestCase):

    """Class for testing user replies"""
    
    def test_if_json_data(self):
        """
            Test for json data
        """
        with self.client:
            token = self.get_token()
            response = self.post_reply(token, 1, 1, "Use static methods")
            self.assertTrue(response.content_type == 'application/json')
            
    def test_reply_class(self):
        """Test for existence of reply model"""
        reply = Reply(1, 1, 'install flask')
        self.assertTrue(reply)
    
    def test_json_data_error_response(self):
        """
            Test error message if not json data provided
        """
        with self.client:
            token = self.get_token()
            response = self.post_reply(token, 1, 1, "Use static methods")
            data = json.loads(response.data.decode())
            self.assertNotEqual(data.get('message'), "Request should be json")
    
    def test_json_data_error_response_code(self):
        """
            Test response code if not json data provided
        """
        with self.client:
            token = self.get_token()
            response = self.post_reply(token, 1, 1, "Use static methods")
            self.assertNotEqual(response.status_code, 400)

    def test_successful_replying(self):
        """
            Test for successful posting of 
            user repplies for a specific question
        """
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            response = self.post_reply(token, 1, 1, "Use static methods")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['reply'])

    def test_replying_to_non_existing_question(self):
        """Test for trying to replying 
            to a question that doesn't exist
        """
        with self.client:
            token = self.get_token()
            response = self.post_reply(token, 1, 1, "Use static methods")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get("message"), "Question not found")
    
    def test_delete_reply(self):
        """Test  if a reply can be deleted"""
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, 1, "Use static methods")
            response = self.delete_reply(token, 1, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['Replies left'], [])

    def test_unauthorized_delete_of_a_reply(self):
        """Test if a non-registered user can delete a reply"""
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, 1, "Use static methods")
            response = self.delete_reply('token', 1, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Invalid token. Please log in again.')
        
    def test_delete_replies(self):
        """Test  if all replies can be deleted at once"""
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, 1, "Use static methods")
            response = self.delete_all_replies(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['Replies left'], [])

    def test_unauthorized_delete_of_all_replies(self):
        """Test if an unauthorized user can delete a reply"""
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, 1, "Use static methods")
            response = self.delete_all_replies('token', 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), 'Invalid token. Please log in again.')
    
    def test_get_all_replies_status_code(self):
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, 1, "Use static methods")
            response = self.get_all_replies(token, 1)
            self.assertEqual(response.status_code, 200)

    def test_get_all_replies(self):
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, 1, "Use static methods")
            response = self.get_all_replies(token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['replies'])

    def test_get_one_reply(self):
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, 1, "Use static methods")
            response = self.get_one_reply(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['reply'])