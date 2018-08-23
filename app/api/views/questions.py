from flask import Blueprint, request, jsonify, make_response
from app.api.models.user import users_list
from app.api.models.questions import Question, qtns_list
from app.api.models.user import User
from app import generate_id
from app.api.views.decorators import login_required


questions = Blueprint('questions', __name__)

@questions.route('/api/v1/questions', methods=['POST'])
@login_required
def post_question(user_id):
    if not request.get_json():
        return make_response(jsonify({"message": "Request should be json"}), 400)
    title = request.get_json()['title']
    subject = request.get_json()['subject']
    qtn_desc = request.get_json()['qtn_desc']
    user_id = request.get_json()['user_id']
    qtn_instance = Question(
                title=title,
                subject=subject,
                qtn_desc=qtn_desc,
                user_id=user_id
            )
    
    qtn_made = User.create_qtn(qtn_instance)
    return jsonify(qtn_made), 201

@questions.route('/api/v1/questions', methods=['GET'])
@login_required
def get_all_questions(user_id):
    if qtns_list:
        return jsonify({"questions": qtns_list})
    return jsonify({"message": "No questions found"})

@questions.route('/api/v1/questions/<int:qtn_id>', methods=['PUT'])
@login_required
def edit_question(user_id, qtn_id):
    if not request.get_json():
        return make_response(jsonify({"message": "Request should be json"}), 400)
    title = request.get_json()['title']
    subject = request.get_json()['subject']
    qtn_desc = request.get_json()['qtn_desc']
    user_id = request.get_json()['user_id']

    updated_qtn = User.update_qtn(
        qtn_id,
        title = title,
        subject = subject,
        qtn_desc = qtn_desc,
        user_id = user_id

    )
    return jsonify({'Updated': updated_qtn}), 200

@questions.route('/api/v1/question/<int:qtn_id>', methods=['DELETE'])
@login_required
def del_qtn(user_id, qtn_id):
    for count, question in enumerate(qtns_list):
        if qtn_id == question['qtn_id']:
            qtns_list.pop(count)
            return jsonify({"questions": qtns_list})
    return jsonify({"message": "No questions found"})

@questions.route('/api/v1/question/<int:qtn_id>', methods=['GET'])
@login_required
def get_one_question(user_id, qtn_id):
    for question in qtns_list:
        if qtn_id == question['qtn_id']:
            return jsonify(question)
    return jsonify({"message": "question not found"})

@questions.route('/api/v1/questions', methods=['DELETE'])
@login_required
def del_all_qtn(user_id):
    if qtns_list:
        qtns_list.clear()
        return jsonify({'Replies left': qtns_list}) 
    return jsonify({'message': 'List empty'})

