import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app import config
from app.models import db, UserData
from app.api import api_bp
from app.auth import auth_bp
from app.cli import cli_bp


server = Flask(__name__)
CORS(server, resources={r"/api/*": {"origins": r"https?://localhost:\d+"}})

if os.environ.get("FLASK_ENV") == "development":
    server.config.from_object(config.DevConfig)
else:
    server.config.from_object(config.ProdConfig)
db.init_app(server)
migrate = Migrate(server, db)

server.register_blueprint(api_bp)
server.register_blueprint(auth_bp)
server.register_blueprint(cli_bp)

# init Folder
with server.app_context():
    db.create_all()
    if not UserData.query.filter_by(name="", owner=None).first():
        UserData.initRoot(None)
        print(">>> Root folder created.")

if __name__ == "__main__":
    server.run()
