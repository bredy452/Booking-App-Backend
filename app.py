from flask import Flask, jsonify, after_this_request
from resources.users import users
from resources.schedules import schedules
import models
from flask_cors import CORS
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
PORT = 8000
app = Flask(__name__)

app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)

CORS(users, origins= ['http://localhost:3000','https://convenientbooking-app-frontend.herokuapp.com'], supports_credentials=True)
CORS(schedules, origins= ['http://localhost:3000', 'https://convenientbooking-app-frontend.herokuapp.com' ], supports_credentials=True)

app.secret_key = os.environ.get('FLASK_APP_SECRET')
# app.secret_key = "hello"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	print("CHECK ME OUT", user_id)
	if hasattr(user_id, 'org_name'):
		# models.Client.get(models.Client.id == user_id)
		return models.Client.get(models.Client.id == user_id)
	
	else:
		return models.Org_user.get(models.Org_user.id == user_id)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(schedules, url_prefix='/schedules')

@app.before_request 
def before_request(): 
    print("you should see this before each request")
    models.DATABASE.connect()

    @after_this_request 
    def after_request(response):
        print("you should see this after each request") 
        models.DATABASE.close()
        return response 


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

if os.environ.get('FLASK_ENV') != 'development':
  	print('\non heroku!')
  	models.initialize()