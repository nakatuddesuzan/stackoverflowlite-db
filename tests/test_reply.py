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
            response = self.post_reply(token, 1,  "Use static methods")
            print(response)
            self.assertTrue(response.content_type == 'application/json')
            
    def test_reply_class(self):
        """Test for existence of reply model"""
        reply = Reply(1, 1, 'install flask')
        self.assertTrue(reply)
    
    
    def test_json_data_error_response_code(self):
        """
            Test response code if not json data provided
        """
        with self.client:
            token = self.get_token()
            response = self.post_reply2(token, 1, "Use static methods")
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get("message"), "Request should be json")

    def test_successful_replying(self):
        """
            Test for successful posting of 
            user repplies for a specific question
        """
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            response = self.post_reply(token, 1, "Use static methods")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get("message"), "Your reply has been posted")
            self.assertEqual(response.status_code, 201)
    
    def test_delete_reply(self):
        """Test  if a reply can be deleted"""
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, "Use static methods")
            response = self.delete_reply(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Your Reply has been deleted")
    
    def test_delete_reply_for_a_non_existent_question(self):
        """Test trying to delete a reply whose question was deleted"""
        with self.client:
            token = self.get_token()
            self.post_reply(token, 1, "Use static methods")
            response = self.delete_reply2(token, 2)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "The reply you are trying to delete doesn't exist")
            self.assertEqual(response.status_code, 400)
    
    def test_update_reply(self):
        """Test  if a reply can be updated"""
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            self.post_reply(token, 1, "Use static methods")
            response = self.edit_reply(token, 1, 1, "Use class methods")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Reply Edited successfully")

    def test_update_a_non_existent_reply(self):
        """
           Test  what happens when one 
           tries to edit a reply that nolonger exixts
        """
        with self.client:
            token = self.get_token()
            self.post_question(token, 1, "flask", "python", "importing files")
            response = self.edit_reply(token, 1, 1, "Use class methods")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "The reply doesn't exist")
    
    def test_mark_preffered_answer(self):
        """Test if a preffered answer can be marked"""
        with self.client:
            token = self.get_token()
            self.post_reply(token, 1, "Use static methods")
            response = self.mark_preffered_answer(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Answer marked as prefferd")
    
    def test_mark_a_non_existent_preffered_answer(self):
        """what happens when a user tries to 
            mark an answer that doesn't exist
        """
        with self.client:
            token = self.get_token()
            response = self.mark_preffered_answer(token, 1, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "This reply has been deleted by the owner")
    
    

