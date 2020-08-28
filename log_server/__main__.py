import os

# from log_server import app, db
# from log_server.server_routes import api


from log_server import db
from log_server.app import app, socketio

# app.register_blueprint(api, url_prefix=url_prefix)

if __name__ == '__main__':
    db.create_all()
    # app.run(host='0.0.0.0', port=3000, debug=True)
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)
