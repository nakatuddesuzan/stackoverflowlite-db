from pprint import pprint
import logging

from flask import jsonify, make_response
from app.config import app_config

from app.api.db_manager.db_config import DatabaseConnection
from app.api.models.user import User

class Question(User, DatabaseConnection):
    
    """Model to fine the structure of a user Question"""

    def __init__(self,qtn_id,user_id,title, subject, qtn_desc):
        DatabaseConnection.__init__(self)
        self.user_id = user_id
        self.qtn_id = qtn_id
        self.title = title
        self.subject = subject
        self.qtn_desc = qtn_desc
        
    @property
    def qtn_desc(self): 
        return self._qtn_desc
    
    @qtn_desc.setter
    def qtn_desc(self, value):
        if not value:
            raise Exception("Field can't be empty")
        self._qtn_desc = value

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
                    return make_response(jsonify({"message": "Question already exists"}))
                else:
                    cursor.execute(sql, (self.user_id, self.title, self.subject, self.qtn_desc))
                    cursor.execute("SELECT * FROM questions WHERE title = '%s'" % self.title)
                    return make_response(jsonify({"message": "Question created successfully"}), 201)
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
        

    @staticmethod
    def update_qtn(qtn_id, title, subject, qtn_desc):
        """This method enables a user to update question by id"""
        try:
            with DatabaseConnection() as cursor:
                sql = "UPDATE questions SET title = %s, subject = %s, qtn_desc = %s WHERE qtn_id = %s RETURNING *"
                question = cursor.execute(sql, (title, subject, qtn_desc, qtn_id))

                if question:
                    return{"update": Question.qtn_dict(question)}
        except Exception as e:
            logging.error(e)
            return make_response(jsonify({'message': str(e)}), 500)
    
    @staticmethod
    def delete_question(qtn_id, user_id):
        with DatabaseConnection() as cursor:
            try:
                query = "SELECT * FROM questions WHERE qtn_id = '%s'" % qtn_id
                cursor.execute(query)
                question = cursor.fetchone()
                print(question)
                if not question:
                    return {"message": "Question doesn't exist"}
                sql = "DELETE FROM questions WHERE qtn_id = %s AND user_id = %s"
                cursor.execute(sql, [qtn_id, user_id])
                return {"message": "Question deleted"}
            except Exception as e:
                return e

    @staticmethod
    def fetch_by_id(user_id, qtn_id):
        try:
            with DatabaseConnection() as cursor:
                sql = "SELECT *  from questions  WHERE qtn_id = %s"
                cursor.execute(sql, [qtn_id])
                result =  cursor.fetchone()
                print(result)
                if result:
                    return result
                return{"message":"question not found"}
        except Exception as e:
            return e
