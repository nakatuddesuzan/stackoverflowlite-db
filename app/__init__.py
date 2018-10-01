import click

from flask import Flask
from flask.cli import with_appcontext
from flasgger import Swagger
from .config import app_config
from flask_cors import CORS
from app.api.db_manager.db_config import DatabaseConnection


app = Flask(__name__, instance_relative_config = True)
app.config.from_object(app_config["development"])
CORS(app)

@app.cli.command('create_tables')
@with_appcontext
def create_tables():
    with DatabaseConnection() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTs users( user_id SERIAL PRIMARY KEY, username VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(12) NOT NULL, bio VARCHAR(50));
        CREATE TABLE IF NOT EXISTs replies(reply_id SERIAL PRIMARY KEY, qtn_id INT NOT NULL, user_id INT NOT NULL, reply_desc VARCHAR(100) NOT NULL, preffered BOOLEAN NOT NULL DEFAULT FALSE);
        CREATE TABLE IF NOT EXISTs questions(qtn_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, title VARCHAR(100) NOT NULL UNIQUE, subject VARCHAR(200) NOT NULL, qtn_desc VARCHAR(100) NOT NULL);
        """)

app.config['swagger'] = {'swagger': '2.0', 'title': 'StackOverFlow-api',
                         'description': "is a web based app that enables users to \
                         ask questions on the platform and get answers.",
                         'basePath': '', 'version': '0.0.1', 'contact': {
                             'Developer': 'Suzan Nakatudde',
                             'email': 'nakatuddesusan@gmail.com'
                        }, 'license': {
                        }, 'tags': [
                            {
                                'name': 'User',
                                'description': 'The api user'
                            },
                            {
                                'name': 'Questions',
                                'description': 'Question options(post, view, \
                                update, delete) for a user'
                            },
                            {
                                'name': 'Answers',
                                'description': 'Reply added to a question'
                            }]}
              
swagger = Swagger(app)

from app.api.views.user import auth
app.register_blueprint(auth)
from app.api.views.questions import questions
app.register_blueprint(questions)
from app.api.views.reply import answers
app.register_blueprint(answers)
