import logging

from flask import Blueprint, request, jsonify, make_response
from app.api.models.questions import Question
from app.api.models.user import User
from app.api.views.decorators import login_required


questions = Blueprint('questions', __name__)

@questions.route('/api/v1/questions', methods=['POST'])
@login_required
def post_question(user_id):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        title = request.get_json()['title']
        subject = request.get_json()['subject']
        qtn_desc = request.get_json()['qtn_desc']
        user_id = request.get_json()['user_id']
        question = Question('qtn_id', user_id=user_id, title=title, subject=subject, qtn_desc=qtn_desc)
        
        Question.create_questions_table(questions)
        result = Question.create_question(question)
        return result
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/questions', methods=['GET'])
@login_required
def get_all_questions(user_id):
    try:
        output = Question.retrieve_all_questions(user_id)
        print(output)
        return  make_response(jsonify(output), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/questions/<int:qtn_id>', methods=['PUT'])
@login_required
def edit_question(user_id, qtn_id):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        title = request.get_json()['title']
        subject = request.get_json()['subject']
        qtn_desc = request.get_json()['qtn_desc']
        qtn_id = request.get_json()['qtn_id']

        Question.update_qtn(qtn_id, title, subject, qtn_desc)
        return make_response(jsonify({"Message":'Succesfully Updated'}), 201)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/question/<int:qtn_id>', methods=['DELETE'])
@login_required
def del_qtn(user_id, qtn_id):
    try:
        output = Question.delete_question(qtn_id, user_id)
        return make_response(jsonify(output), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/question/<int:qtn_id>', methods=['GET'])
@login_required
def get_one_question(user_id, qtn_id):
    try:
        output = Question.fetch_by_id(user_id, qtn_id)
        return make_response(jsonify({"question": output}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)
