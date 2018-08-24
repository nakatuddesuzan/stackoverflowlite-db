import psycopg2
from pprint import pprint
from flask import current_app as app

class DatabaseConnection():

    def __init__(self, database_url):
        try:
            self.conn = psycopg2.connect(
                "dbname = 'stackoverflow' user = 'postgres' host = 'localhost' password = 'graphics123456789' port = '5432'")
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except:
            pprint("Cannot connect to the database")

    def create_tables(self):
        """Create tables needed"""

        create_tables_commands = (
            """
            CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(100),
                email VARCHAR(100) NOT NULL, 
                password VARCHAR(12) NOT NULL
            )
            """
            """
            CREATE TABLE IF NOT EXISTS questions(
                qtn_id SERIAL PRIMARY KEY,
                user_id SERIAL,
                title VARCHAR(100),
                subject VARCHAR(25)
                description VARCHAR(200)
            )
            """
            """
            CREATE TABLE IF NOT EXISTS replies(
                reply_id SERIAL PRIMARY KEY,
                qtn_id SERIAL PRIMARY KEY,
                user_id SERIAL,
                description VARCHAR(200)
            )
            """
        )
        self.cursor.execute(create_tables_commands)
        self.conn.commit
        self.conn.close


class UserDbQueries(DatabaseConnection):

    def __init__(self):
        DatabaseConnection.__init__(self, app.config['DATABASE_URL'])

    def insert_user_data(self):
        query = (
            """INSERT INTO  users(user_id, username, email, password) 
            VALUES(%(user_id)s, %(username)s, %(email)s, %(password)s) """)
        self.cursor.execute(query)
        self.conn.commit()
        self.conn.close

class QuestionsDbQueries(DatabaseConnection):
    def __init__(self):
        DatabaseConnection.__init__(self, app.config['DATABASE_URL'])

    def insert_into_questions(self):
        query = (
            """INSERT INTO  questions(user_id, qtn_id, title, subject, description) 
            VALUES(%(qtn_id)s, %(user_id)s, %(title)s, %(subject)s, %(description)s) """)
        self.cursor.execute(query)
        self.conn.commit()
    
    def query_all(self):
        self.cursor.execute("""SELECT * from questions""")
        questions = []
        rows = self.cursor.fetchall()
        pprint('Questions: ', self.cursor.rowcount)
        for row in rows:
            questions.append(row)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def update_question_record(self):
        try:
            update_command = """UPDATE question SET status = '{}' WHERE id = '{}'
                                .format(data['status'], qtn_id)
                            """
            self.cursor.execute(update_command)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            pprint(error)
        finally:
            if self.conn is not None:
                self.conn.close()
 
        
    def fetch_by_id(self):
        try:
            self.cursor.execute(
                "SELECT qtn_id, user_id, title, subject, description from questions order by qtn_id"
            )
            pprint("question: ", self.cursor.rowcount)
            #fetch one row
            row = self.cursor.fetchone()
            while row is not None:
                pprint(row)
                row = self.cursor.close()
            self.cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
    
    def delete_a_question(self, qtn_id):
        """Delete question by id"""
        self.conn = None
        rows_deleted = 0
        try:
            self.cursor.execute("DELETE FROM questions WHERE qtn_id = %s", (qtn_id,))
            # get the number of updated rows
            rows_deleted = self.cursor.rowcount
            # Commit the changes to the database
            self.conn.commit()
            # Close communication with the PostgreSQL database
            self.cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            pprint(error)
        finally:
            if self.conn is not None:
                self.conn.close()
 
        return rows_deleted

class ReplyDbQueries(DatabaseConnection):
    def __init__(self):
        DatabaseConnection.__init__(self, app.config['DATABASE_URL'])
    
    def insert_into_replies(self):
        try:
            query = (
                    """INSERT INTO  replies(user_id, qtn_id, description) 
                    VALUES(%(qtn_id)s, %(user_id)s, %(description)s) """)
            self.cursor.execute(query)
            self.cursor.close()
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            pprint(error)
        finally:
            if self.conn is not None:
                self.conn.close()