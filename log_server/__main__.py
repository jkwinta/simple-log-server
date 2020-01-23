import os

from log_server import app, db
from log_server.server_routes import api

url_prefix = os.environ.get('LOGGER_URL_PREFIX', '/')

app.register_blueprint(api, url_prefix=url_prefix)

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=3000, debug=True)
