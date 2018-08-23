from flask import Flask
from .config import app_config


app = Flask(__name__, instance_relative_config = True)
app.config.from_object(app_config["development"])

"""
This function enables to  automatically generater ids for
list items
"""

id = 0


def generate_id(_list):
    global id
    if len(_list) == 0:
        id = len(_list) + 1
    else:
        id = id + 1
    return id

from app.api.views.user import auth
app.register_blueprint(auth)
from app.api.views.questions import questions
app.register_blueprint(questions)
from app.api.views.reply import answers
app.register_blueprint(answers)
