from pprint import pprint

from flask import jsonify
from app.config import app_config

from app.api.db_manager.db_config import DatabaseConnection
from app.api.models.user import User
from app.api.models import check_users

class Question(User, DatabaseConnection):
    
    """Model to fine the structure of a user Question"""

    def __init__(self,qtn_id,user_id,title, subject, qtn_desc):
        DatabaseConnection.__init__(self)
        self.user_id = user_id
        self.qtn_id = qtn_id
        self.title = title
        self.subject = subject
        self.qtn_desc = qtn_desc

    def create_questions_table(self):
        try:
            with DatabaseConnection() as cursor:
                sql = "CREATE TABLE IF NOT EXISTs questions(qtn_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, title VARCHAR(100) NOT NULL UNIQUE, subject VARCHAR(200) NOT NULL, qtn_desc VARCHAR(100) NOT NULL)"
                cursor.execute(sql)
        except Exception as e:
            return e

    def create_question(self):
        sql = "INSERT INTO  questions(user_id, title, subject, qtn_desc) VALUES(%s, %s, %s, %s) RETURNING title"
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT * FROM questions WHERE title = '%s'" % self.title)
                
                if cursor.fetchone():
                    return {"message": "Question already exists"}
                else:
                    cursor.execute(sql, (self.user_id, self.title, self.subject, self.qtn_desc))
                    cursor.execute("SELECT * FROM questions WHERE title = '%s'" % self.title)
                    self.conn.commit()
                    result_qtn = cursor.fetchone()
                    print(self.qtn_dict(result_qtn))
                    return {"message": self.qtn_dict(result_qtn),
                        "status":201}
        except Exception as e:
            return e

    @staticmethod
    def retrieve_all_questions(user_id):
        results = []
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT * FROM questions")
                questions = cursor.fetchall()
                if questions:
                    for question in questions:
                        results.append(Question.qtn_dict(question))
                    return results
                return {'message':'No questions found'}
        except Exception as e:
            return e

    @staticmethod
    def qtn_dict(question):
        return{
            "qtn_id": question[0],
            "user_id": question[1],
            "title": question[2],
            "subject": question[3],
            "qtn_desc":  question [4]
        }

    def update_question(self):
        pass