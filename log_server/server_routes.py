import json
import os

from log_server.message import Message
from flask import Blueprint, request, Response
from log_server import db

api = Blueprint('logger', __name__)

MAX_MESSAGES = os.environ.get('MAX_MESSAGES')
try:
    MAX_MESSAGES = int(MAX_MESSAGES)
except:
    MAX_MESSAGES = None


@api.route('/log', methods=('POST',))
def log_message():
    # TODO: Delete oldest messages if message count exceeds MAX_MESSAGES
    # force in case it doesn't have Content-Type="application/json"
    content = request.get_json(silent=True, force=True)

    message = content.get('message', '')

    try:
        message = json.dumps(message)
    except:
        message = str(message)

    new_message = Message(message=str(message))
    db.session.add(new_message)
    db.session.commit()
    return Response('200')


@api.route('/clear', methods=('POST',))
def clear_messages():
    # TODO: clear messages
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
