# from log_server import app
from log_server.message import Message
from flask import Blueprint, request

api = Blueprint('logger', __name__)


@api.route('/log', methods=('POST',))
def log_message():
    # force in case it doesn't have Content-Type="application/json"
    content = request.get_json(silent=True, force=True)
    print(content)
    # new_message = Message()
    # return 'log_message'


@api.route('/clear', methods=('POST',))
def clear_messages():
    return 'clear_messages'


@api.route('/messages', methods=('GET',))
def get_messages():
    return 'get_messages'

# db.session.add(User(name="Flask", email="example@example.com"))
# db.session.commit()
#
# users = User.query.all()
