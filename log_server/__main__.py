from log_server import app
from log_server.server_routes import api

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
