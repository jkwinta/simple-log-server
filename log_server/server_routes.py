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
    messages = Message.query.all()
    message_strings = []
    for message in messages:
        local_time = message.get_local_time()
        if local_time is not None:
            local_time_str = local_time.isoformat()
        else:
            local_time_str = local_time
        # TODO: parse json and embed?
        message_strings.append('{} : {}'.format(local_time_str, message.message))
    result = '<br>'.join(message_strings)
    return result
