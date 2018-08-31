import logging
from app.api.models.questions import Question
from app.api.db_manager.db_config import DatabaseConnection
from flask import jsonify, make_response
from app.api.models.user import User

class Reply(Question, User, DatabaseConnection):
    def __init__(self, user_id, qtn_id, reply_desc):
        DatabaseConnection.__init__(self)
        self.qtn_id = qtn_id
        self.user_id = user_id
        self.reply_desc = reply_desc

    def create_replies_table(self):
        sql = "CREATE TABLE IF NOT EXISTs replies(reply_id SERIAL PRIMARY KEY, qtn_id INT NOT NULL, user_id INT NOT NULL, reply_desc VARCHAR(100) NOT NULL)"
        self.cursor.execute(sql)

    def post_reply(self):
        sql = "INSERT INTO replies(qtn_id, user_id, reply_desc) VALUES( %s, %s, %s) RETURNING qtn_id"
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(sql, (self.qtn_id, self.user_id, self.reply_desc))
                cursor.execute("SELECT * FROM replies WHERE qtn_id = '%s'" % self.qtn_id)
                cursor.fetchone()
                return make_response(jsonify({"message": "Your reply has been posted"}), 200)
        except Exception as e:
            raise e

    @staticmethod
    def reply_dict(reply):
        return{
            "reply_id": reply[0],
            "qtn_id": reply[1],
            "user_id":reply[2],
            "reply_desc": reply[3]
        }
    
    @staticmethod
    def check_approve_status(reply_id):
        """check the status of the reply whether approved or not"""
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT approve FROM replies WHERE reply_id = '%s'", [reply_id])
            approve = cursor.fetchone()
            if approve =="Yes":
                return "Best answer"
   
    @staticmethod
    def delete_reply(reply_id, qtn_id, user_id):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT * FROM replies WHERE reply_id = %s AND qtn_id = %s", [reply_id, qtn_id])
                response1 = cursor.fetchone()
                if not response1:
                    return make_response(jsonify({"message": "The reply you are trying to delete doesn't exist"}), 404)
                else:
                    cursor.execute("DELETE FROM replies where reply_id = %s AND qtn_id = %s", [reply_id, qtn_id])
                    return jsonify({"message": "Your Reply has been deleted"})
        except Exception as e:
            raise e

    @staticmethod
    def edit_reply(reply_id, qtn_id, user_id, reply_desc):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT * FROM replies WHERE reply_id = %s AND qtn_id = %s", [reply_id, qtn_id])
                if not cursor.fetchone():
                    return make_response(jsonify({"message": "The reply doesn't exist"}), 400)
                sql = "UPDATE replies SET reply_desc = %s where reply_id = %s AND qtn_id = %s"
                cursor.execute(sql, [reply_desc, reply_id, qtn_id])
                return jsonify({"message":"Reply Edited successfully"})
        except Exception as e:
            raise e