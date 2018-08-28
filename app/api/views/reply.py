import logging

from flask import Blueprint, request, jsonify, make_response
from app.api.models.questions import Question
from app.api.models.user import User
from app.api.models.reply import Reply
from app.api.views.decorators import login_required

answers = Blueprint('answers', __name__)


@answers.route('/api/v1/question/<int:qtn_id>/answer', methods=['POST'])
@login_required
def post_answer(user_id, qtn_id):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        qtn_id = request.get_json()['qtn_id']
        user_id = request.get_json()['user_id']
        approve = request.get_json()['approve']
        reply_desc = request.get_json()['reply_desc']
        reply_instance = Reply(user_id, qtn_id, reply_desc, approve)
        print(reply_instance)

        reply = Reply.post_reply(reply_instance)
        print(reply)
        return reply
       
    except Exception as e:
        raise e
        # logging.error(e)
        # return make_response(jsonify({'message': str(e)}), 500)
