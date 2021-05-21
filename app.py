from flask import Flask, jsonify
from resources.users import users
import models
from flask_cors import CORS
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
PORT = 8000
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return models.Org_user.get(models.Org_user.id == user_id)

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/users')


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)