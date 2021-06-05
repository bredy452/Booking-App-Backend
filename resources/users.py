import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user, current_user, login_required


users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
@login_required
def user_list():
	user_org_dicts = [model_to_dict(org) for org in models.Org_user.select()]
	user_client_dicts = [model_to_dict(client) for client in models.Client.select()]

	return jsonify({
		'data': [user_org_dicts, user_client_dicts], 
		'message': f'Successfully found {len(user_org_dicts)} Organization Users and {len(user_client_dicts)} Client users',
		'status': 200
		}), 200

@users.route('/organizations', methods=['GET'])
def organizations():
	org_dicts = [model_to_dict(org) for org in models.Org_user.select()]
	
	return jsonify({
		'organizations': [org_dicts],
		'message': f'Successfully found {len(org_dicts)} Organization Users',
		'status': 200
	}), 200

#Routes for organization users	
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
		created_org_user = models.Org_user.create(
			**payload
		)

	login_user(created_org_user)

	created_org_user_dict = model_to_dict(created_org_user)
	created_org_user_dict.pop('password')

	return jsonify(
		data = created_org_user_dict,
		message = "Successfull registered organization user",
		status = 201
	), 201

@users.route('/org_user/login', methods=['POST'])
def login_org_():
	payload = request.get_json()
	try:
		org_user = models.Org_user.get(models.Org_user.username == payload['username'])
		user_org_dict = model_to_dict(org_user)
		password_is_good = check_password_hash(user_org_dict['password'], payload['password'])

		if (password_is_good):
			login_user(org_user)
			user_org_dict.pop('password')

			return jsonify(
				data = user_org_dict,
				message = f"Successfully loggin in {user_org_dict['username']}",
				status = 200

			), 200
		else:
			return jsonify(
				data = {},
				message = "Email or password is incorrect",
				status = 401
			), 401
	except models.DoesNotExist:
		return jsonify(
			data = {},
			message = "Email or password is incorrect",
			status = 401
		), 401


#Routes for client users
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

@users.route('/client/login', methods=['POST'])
def login_client():
	payload = request.get_json()
	try:
		client_user = models.Client.get(models.Client.username == payload['username'])
		user_client_dict = model_to_dict(client_user)
		password_is_good = check_password_hash(user_client_dict['password'], payload['password'])

		if (password_is_good):
			login_user(client_user)
			user_client_dict.pop('password')

			return jsonify(
				data = user_client_dict,
				message = f"Successfully loggin in {user_client_dict['username']}",
				status = 200

			), 200
		else:
			return jsonify(
				data = {},
				message = "Email or password is incorrect",
				status = 401
			), 401
	except models.DoesNotExist:
		return jsonify(
			data = {},
			message = "Email or password is incorrect",
			status = 401
		), 401

@users.route('/logout', methods=['GET'])
def logout():
	logout_user()

	return jsonify(
		data = {},
		message = 'User successfully logged out',
		status = 200
	), 200