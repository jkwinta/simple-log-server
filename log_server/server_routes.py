# from log_server import app
from log_server.message import Message
from flask import Blueprint, request
from log_server import db

api = Blueprint('logger', __name__)


@api.route('/log', methods=('POST',))
def log_message():
    # force in case it doesn't have Content-Type="application/json"
    content = request.get_json(silent=True, force=True)
    keys = [col.key for col in Message.__table__.columns]

    new_message = Message(**{k: v for k, v in content.items() if k in keys})
    db.session.add(new_message)
    db.session.commit()


@api.route('/clear', methods=('POST',))
def clear_messages():
    return 'clear_messages'


@api.route('/messages', methods=('GET',))
def get_messages():
    result = Message.query.all()
    return 'get_messages'

# db.session.add(User(name="Flask", email="example@example.com"))
# db.session.commit()
#
# users = User.query.all()
