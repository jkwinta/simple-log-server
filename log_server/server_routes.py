import json
import os

from log_server.message import Message
from flask import Blueprint, request, Response, render_template
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


@api.route('/clear', methods=('POST', 'GET'))
def clear_messages():
    n_del = db.session.query(Message).delete()
    db.session.commit()
    return render_template('clear_messages.html', n_del=n_del)


@api.route('/messages', methods=('GET',))
def get_messages():
    messages = Message.query.all()
    formatted_messages = []
    for message in messages:
        local_time = message.get_local_time()
        if local_time is not None:
            local_time_str = local_time.isoformat()
        else:
            local_time_str = local_time
        # TODO: parse json and embed?
        formatted_messages.append({'time': local_time_str,
                                   'message': message.message})
    return render_template('messages.html', messages=formatted_messages)
