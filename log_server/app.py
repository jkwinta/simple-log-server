from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit

from log_server.message import Message
from flask import Blueprint, request, Response, render_template
from log_server import db, app

socketio = SocketIO(app)


# @socketio.on('connect')
# def test_connect():
#     emit('after connect', {'data': 'Lets dance'})


# @socketio.on('message', namespace='/ws')
# def on_message_ws(message):
#     print('ws message {}'.format(message))


# api = Blueprint('logger', __name__)

def make_message_out(message):
    local_time = message.get_local_time()
    if local_time is not None:
        local_time_str = local_time.isoformat()
    else:
        local_time_str = local_time
    return {
        'time': local_time_str,
        'message': message.message,
    }


@app.route('/', methods=('GET',))
def index_forward():
    return redirect(url_for('get_messages'))


@app.route('/log', methods=('POST',))
def log_message():
    # force in case it doesn't have Content-Type="application/json"
    content = request.get_json(silent=True, force=True)

    message = content.get('message', '')

    # try:
    #     message = json.dumps(message)
    # except:
    #     message = str(message)

    if Message:
        pass

    new_message = Message(message=str(message))
    db.session.add(new_message)
    db.session.commit()
    socketio.emit('message', make_message_out(new_message), namespace='/ws')
    return Response('200')


@app.route('/clear', methods=('POST', 'GET'))
def clear_messages():
    n_del = db.session.query(Message).delete()
    db.session.commit()
    return render_template('clear_messages.html', n_del=n_del)


@app.route('/messages', methods=('GET',))
def get_messages():
    messages = Message.query.all()
    formatted_messages = []
    for message in messages:
        formatted_messages.append(make_message_out(message))
    return render_template('messages.html', messages=formatted_messages)


if __name__ == '__main__':
    db.create_all()
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)
