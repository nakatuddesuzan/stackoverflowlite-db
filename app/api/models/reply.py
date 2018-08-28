import logging
from app.api.models.questions import Question
from app.api.db_manager.db_config import DatabaseConnection
from flask import jsonify, make_response

class Reply(Question, DatabaseConnection):
    def __init__(self, user_id, qtn_id, reply_desc, approve):
        DatabaseConnection.__init__(self)
        self.reply_desc = reply_desc
        self.qtn_id = qtn_id
        self.user_id = user_id
        self.approve = approve

    def create_replies_table(self):
        sql = "CREATE TABLE IF NOT EXISTs replies(reply_id SERIAL PRIMARY KEY, qtn_id INT NOT NULL, user_id INT NOT NULL, reply_desc VARCHAR(100) NOT NULL, approve VARCHAR(100)NOT NULL)"
        self.cursor.execute(sql)

    def post_reply(self):
        sql = "INSERT INTO replies(qtn_id, user_id, reply_desc, approve) VALUES(%s, %s, %s, %s) RETURNING qtn_id"
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(sql, (self.qtn_id, self.user_id, self.reply_desc, self.approve))
                cursor.execute("SELECT * FROM replies WHERE qtn_id = '%s'" % self.qtn_id)
                result = cursor.fetchone()
                return jsonify(self.reply_dict(result))
        except Exception as e:
            raise e


    @staticmethod
    def reply_dict(reply):
        return{
            "reply_id": reply[0],
            "qtn_id": reply[1],
            "user_id":reply[2],
            "reply_desc": reply[3],
        }
    
    @staticmethod
    def check_approve_status(reply_id):
        """check the status of the reply whether approved or not"""
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT approve FROM replies WHERE reply_id = '%s'", [reply_id])
            approve = cursor.fetchone()
            if approve =="Yes":
                return "Best answer"
   
    