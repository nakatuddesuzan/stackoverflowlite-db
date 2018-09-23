import logging

from flask import Blueprint, request, jsonify, make_response
from flasgger import swag_from
from app.api.models.questions import Question
from app.api.models.user import User
from app.api.views.decorators import login_required


questions = Blueprint('questions', __name__)

@questions.route('/api/v1/questions', methods=['POST'])
@login_required
@swag_from("../docs/post_question.yml")
def post_question(user):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        title = request.get_json()['title'].strip()
        subject = request.get_json()['subject'].strip()
        qtn_desc = request.get_json()['qtn_desc'].strip()
        question = Question('qtn_id', user.user_id, title=title, subject=subject, qtn_desc=qtn_desc)
        
        Question.create_questions_table(questions)
        result = Question.create_question(question)
        return result
    except Exception as e:
        raise e

@questions.route('/api/v1/questions', methods=['GET'])
@login_required
@swag_from("../docs/get_all_questions.yml")
def get_all_questions(user):
    try:
        output = Question.retrieve_all_questions(user.user_id)
        return  make_response(jsonify(output), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/questions/<int:qtn_id>', methods=['PUT'])
@login_required
@swag_from("../docs/edit_question.yml")
def edit_question(user_id, qtn_id):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        title = request.get_json()['title'].strip()
        subject = request.get_json()['subject'].strip()
        qtn_desc = request.get_json()['qtn_desc'].strip()
        qtn_id = request.get_json()['qtn_id']

        Question.update_qtn(qtn_id, title, subject, qtn_desc)
        return make_response(jsonify({"Message":'Succesfully Updated'}), 201)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/question/<int:qtn_id>', methods=['DELETE'])
@login_required
@swag_from("../docs/delete_question.yml")
def del_qtn(user, qtn_id):
    try:
        output = Question.delete_question(qtn_id, user.user_id)
        return make_response(jsonify(output), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/question/<int:qtn_id>', methods=['GET'])
@login_required
@swag_from("../docs/get_one_question.yml")
def get_one_question(user, qtn_id):
    try:
        output = Question.fetch_by_id(user.user_id, qtn_id)
        return make_response(jsonify(output), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)
