from flask import make_response, jsonify
from app import app

@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"message": "Page not found, Please check your URL"}), 404)

@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'message':'Requested method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True)
