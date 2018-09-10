import logging

from flask import Blueprint, request, jsonify, make_response, g
from app.api.models.questions import Question
from app.api.models.user import User
from app.api.views.decorators import login_required


questions = Blueprint('questions', __name__)

@questions.route('/api/v1/questions', methods=['POST'])
@login_required
def post_question():
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        title = request.get_json()['title'].strip()
        subject = request.get_json()['subject'].strip()
        qtn_desc = request.get_json()['qtn_desc'].strip()
        # user = g.user
        question = Question( "qtn_id", g.user["user_id"] ,title=title, subject=subject, qtn_desc=qtn_desc)
        print(question)

        Question.create_questions_table(questions)
        result = Question.create_question(question)
        print (result)
        return result
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/questions', methods=['GET'])
@login_required
def get_all_questions():
    try:
        current_user = g.user
        output = Question.retrieve_all_questions(current_user)
        return  make_response(jsonify(output), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/questions/<int:qtn_id>', methods=['PUT'])
@login_required
def edit_question(qtn_id):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        title = request.get_json()['title'].strip()
        subject = request.get_json()['subject'].strip()
        qtn_desc = request.get_json()['qtn_desc'].strip()

        current_user = g.user
        Question.update_qtn(current_user, qtn_id, title, subject, qtn_desc)
        return make_response(jsonify({"Message":'Succesfully Updated'}), 201)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/question/<int:qtn_id>', methods=['DELETE'])
@login_required
def del_qtn(qtn_id):
    try:
        current_user = g.user
        output = Question.delete_question(qtn_id, current_user)
        return make_response(jsonify(output), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@questions.route('/api/v1/question/<int:qtn_id>', methods=['GET'])
@login_required
def get_one_question(qtn_id):
    try:
        current_user = g.user
        output = Question.fetch_by_id(current_user, qtn_id)
        return make_response(jsonify({"question": output}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)
