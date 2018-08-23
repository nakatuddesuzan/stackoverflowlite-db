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
            CREATE TABLE users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(100),
                email VARCHAR(100) NOT NULL, 
                password VARCHAR(12) NOT NULL
            )
            """
            """
            CREATE TABLE questions(
                qtn_id SERIAL PRIMARY KEY,
                user_id SERIAL,
                title VARCHAR(100),
                subject VARCHAR(25)
                description VARCHAR(200)
            )
            """
            """
            CREATE TABLE replies(
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

