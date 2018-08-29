from flask import Flask
from flasgger import Swagger
from .config import app_config


app = Flask(__name__, instance_relative_config = True)
app.config.from_object(app_config["development"])


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
              
swag = Swagger(app)

from app.api.views.user import auth
app.register_blueprint(auth)
from app.api.views.questions import questions
app.register_blueprint(questions)
from app.api.views.reply import answers
app.register_blueprint(answers)
