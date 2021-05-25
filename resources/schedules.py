import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

schedules = Blueprint('schedules', 'schedules')

@schedules.route('/org_user/addSchedule', methods=['POST'])
def add_schedule():
	payload = request.get_json()
	new_schedule = models.Schedule.create(availability=payload['availability'], org_id=current_user.id)
	schedule_dict = model_to_dict(new_schedule)

	return jsonify(
		data = schedule_dict,
		message = "successfully created schedule",
		status = 201
	), 201

@schedules.route('/org_user/viewSchedule', methods=['GET'])
def view_schedule():
	org_schedule_dicts = [model_to_dict(schedule) for schedule in current_user.schedule]

	return jsonify({
		'data': org_schedule_dicts,
		'message': f'Successfully found {len(org_schedule_dicts)} schedule',
		'status': 200 
	}), 200

