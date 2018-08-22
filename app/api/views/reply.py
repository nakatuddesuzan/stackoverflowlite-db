from flask import Blueprint, request, jsonify, make_response
from app.api.models.user import users_list
from app.api.models.questions import Question, qtns_list
from app.api.models.user import User
from app import generate_id
from app.api.models.reply import Reply, replies_list
from app.api.views.decorators import login_required

answers = Blueprint('answers', __name__)


@answers.route('/api/v1/answer/<int:qtn_id>', methods=['POST'])
@login_required
def post_answer(user_id, qtn_id):
    if not request.get_json():
        return make_response(jsonify({"message": "Request should be json"}), 400)
    reply_desc = request.get_json()['reply_desc']
    qtn_id = request.get_json()['qtn_id']
    for question in qtns_list:
        if qtn_id == question['qtn_id']:
            answer = Reply(user_id=user_id, qtn_id=qtn_id, reply_desc = reply_desc)
            reply_made = User.make_reply(answer)
            return jsonify({'reply': reply_made})  
    return jsonify({"message": "Question not found"})

#endpoint for user to delete replies to his or her question
@answers.route('/api/v1/answers/<int:qtn_id>', methods=['DELETE'])
@login_required
def delete_replies(user_id, qtn_id):
    for question in qtns_list:
        if qtn_id == question['qtn_id']:
            replies_list.clear()
            return jsonify({'Replies left': replies_list}) 
    return jsonify({'message': 'Oooppss something went wrong'})

# #endpoint for user to delete a reply to his or her question
@answers.route('/api/v1/answer/<int:qtn_id>/<int:reply_id>', methods=['DELETE'])
@login_required
def delete_reply(user_id, qtn_id, reply_id):
    for question in qtns_list:
        if qtn_id == question['qtn_id']:
            for count, reply in enumerate(replies_list):
                if reply_id == reply['reply_id']:
                    replies_list.pop(count)
                    return jsonify({'Replies left': replies_list}) 
    return jsonify({'message': 'Oooppss something went wrong'})

@answers.route('/api/v1/answer/<int:qtn_id>', methods=['GET'])
@login_required
def get_all_answers(user_id, qtn_id):
        if replies_list:
            return jsonify({"replies": replies_list})
        return jsonify({"message": "No replies found"})

@answers.route('/api/v1/answer/<int:qtn_id>/<int:reply_id>', methods=['GET'])
@login_required
def get_one_answers(user_id, qtn_id, reply_id):
    for reply in replies_list:
        if reply_id == reply['reply_id']:
            return jsonify({"reply": reply})
    return jsonify({"message": "Reply not found"})
