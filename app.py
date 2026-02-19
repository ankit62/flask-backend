from flask import Flask
from flask_cors import CORS
from routes.users import users_bp
from db.init_db import init_db

app = Flask(__name__)
CORS(app)

app.register_blueprint(users_bp)

#Initialize DB tables startup
init_db()