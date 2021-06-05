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

	return jsonify(
		data = org_schedule_dicts,
		message = f'Successfully found {len(org_schedule_dicts)} schedule',
		status = 200 
	), 200

@schedules.route('/org_user/editSchedule/<id>', methods=['PUT'])
def edit_schedule(id):
	payload = request.get_json()

	models.Schedule.update(**payload).where(models.Schedule.id == id).execute()
	

	# return payload['availability']

	return jsonify(
		data = model_to_dict(models.Schedule.get_by_id(id)),
		message = "successfully updated schedule",
		status = 201
	 ), 201

@schedules.route('/<organization>', methods=['GET'])
def get_one_schedule(organization):
	try:
		record = models.Org_user.get(models.Org_user.org_name == organization)

		schedule = models.Schedule.get(models.Schedule.org_id == record.id)

		return jsonify(
			data = model_to_dict(schedule),
			message = 'Success!!!',
			status = 200
	), 200

	except models.DoesNotExist:
		return jsonify(
			data = {},
			message = "Schedule does not exist",
			status = 200 
		), 200

@schedules.route('/client_schedule/<organization>', methods=['GET'])
def client_schedule(organization):
	try:
		org_id = models.Org_user.get(models.Org_user.org_name == organization)
		record = models.Client_schedule.get(models.Client_schedule.org_id == org_id.id)
	

		return jsonify(
			data = model_to_dict(record),
			message= f'Successfully found',
			status= 200 
		), 200
	except models.DoesNotExist:
		return jsonify(
			data = {},
			message = "Schedule does not exist",
			status = 200 
		), 200


@schedules.route('/org_user/<id>', methods=['DELETE'])
def delete_schedule(id):

	models.Org_user.delete().where(models.Org_user.id==id).execute()

	return jsonify(
		data = None,
		status = 200,
		message = 'schedule deleted successfully'
	), 200

@schedules.route('/client/bookDate', methods=['POST'])
def add_booking_dates():
	print("THIS IS THE CURRENT USER ", current_user)
	payload = request.get_json()
	print("THIS IS PAYLOAD ", payload)
	org_id = models.Org_user.get(models.Org_user.org_name == payload['org_id'])
	print("HEREEE ", org_id)
	booking_dates = models.Client_schedule.create(client_availability=payload['client_availability'], client_id=current_user.id, org_id = org_id.id )
	schedule_dict = model_to_dict(booking_dates)

	# return model_to_dict(org_id)


	return jsonify(
		data = schedule_dict,
		message = "successfully created schedule",
		status = 201
	), 201



