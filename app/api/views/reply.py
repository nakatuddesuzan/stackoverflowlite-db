import logging

from flask import Blueprint, request, jsonify, make_response
from flasgger import swag_from
from app.api.models.questions import Question
from app.api.models.user import User
from app.api.models.reply import Reply
from app.api.views.decorators import login_required

answers = Blueprint('answers', __name__)


@answers.route('/api/v1/question/<int:qtn_id>/answer', methods=['POST'])
@login_required
@swag_from("../docs/add_answer.yml")
def post_answer(user, qtn_id):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        reply_desc = request.get_json()['reply_desc']
        reply_instance = Reply(user.user_id, qtn_id, reply_desc)

        reply = Reply.post_reply(reply_instance)
        return reply
    except Exception as e:
        return e

@answers.route('/api/v1/question/<int:qtn_id>/answer/<int:reply_id>', methods=['PUT'])
@login_required
@swag_from("../docs/edit_answer.yml")
def update_answer(user, qtn_id, reply_id):
    try:
        if not request.get_json():
            return make_response(jsonify({"message": "Request should be json"}), 400)
        reply_desc = request.get_json()['reply_desc']
        response = Reply.edit_reply(reply_id, qtn_id, user.user_id, reply_desc)
        return response
    except Exception as e:
        raise e

@answers.route('/api/v1/question/<int:qtn_id>/answer/<int:reply_id>', methods=['DELETE'])
@login_required
@swag_from("../docs/edit_answer.yml")
def delete_answer(user, qtn_id, reply_id):
    try:
        output = Reply.delete_reply(user.user_id, reply_id, qtn_id)
        return output
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({'message': str(e)}), 500)

@answers.route('/api/v1/question/<int:qtn_id>/answers/<int:reply_id>', methods=['PUT'])
@login_required
@swag_from("../docs/edit_answer.yml")
def mark_best_answer(user, qtn_id, reply_id):
    response = Reply.mark_preferred_answer(user.user_id, reply_id, qtn_id)
    print(response)
    return response