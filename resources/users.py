import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user


users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def user_list():
	user_org_dicts = [model_to_dict(org) for org in models.Org_user.select()]
	user_client_dicts = [model_to_dict(client) for client in models.Client.select()]

	return jsonify({
		'data': [user_org_dicts, user_client_dicts], 
		'message': f'Successfully found {len(user_org_dicts)} Organization Users and {len(user_client_dicts)} Client users',
		'status': 200
		}), 200
	

@users.route('/org_user/register', methods=['POST'])
def register_orgs():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()

	try:
		models.Org_user.get(models.Org_user.email == payload['email'])
		return jsonify(
			data = {},
			message = f"A user with that email already exists",
			status = 401
		), 401
	except models.DoesNotExist:
		payload['password'] = generate_password_hash(payload['password'])
		created_user = models.Org_user.create(
			**payload
		)

	login_user(created_org_user)

	created_org_user_dict = model_to_dict(created_org_user)
	created_org_user_dict.pop('password')

	return jsonify(
		data = created_user_dict,
		message = "Successfull registered organization user",
		status = 201
	), 201

@users.route('/client/register', methods=['POST'])
def register_client():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()

	try:
		models.Client.get(models.Client.email == payload['email'])
		return jsonify(
			data = {},
			message = f"A user with that email already exists",
			status = 401
		), 401
	except models.DoesNotExist:
		payload['password'] = generate_password_hash(payload['password'])
		created_client_user = models.Client.create(
			**payload
		)

	login_user(created_client_user)

	created_client_user_dict = model_to_dict(created_client_user)
	created_client_user_dict.pop('password')

	return jsonify(
		data = created_client_user_dict,
		message = "Successfull registered client user",
		status = 201
	), 201