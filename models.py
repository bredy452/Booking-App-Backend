import os
from playhouse.db_url import connect
from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///booking.sqlite')
# DATABASE = SqliteDatabase('booking.sqlite')



class Org_user(UserMixin, Model):
	org_name = CharField(unique=True)
	first_name = CharField(null=True)
	last_name = CharField(null=True)
	email = CharField(null=False)
	username = CharField(null=False)
	password = CharField(null=False)
	# schedule_id = ForeignKeyField(Schedule, backref='my_schedule')

	class Meta:
		database = DATABASE


class Client(UserMixin, Model):
	first_name = CharField(null=False)
	last_name = CharField(null=False)
	phone_number = CharField(null=False)
	username = CharField(null=False)
	email = CharField(null=False)
	password = CharField(null=False)
	# organization_id = ForeignKeyField(Org_user, backref='my_booking')

	class Meta:
		database = DATABASE

class Client_schedule(Model):
	client_availability = CharField()
	client_id = ForeignKeyField(Client, backref='my_schedule', null=True)
	org_id = ForeignKeyField(Org_user, backref='schedule')

	class Meta:
		database = DATABASE

class Schedule(Model):
	availability = CharField()
	# info = CharField()
	org_id = ForeignKeyField(Org_user, backref='schedule')
	# date = CharField()
	# client_schedule_id = ForeignKeyField(Client_schedule, backref='client_schedule', null=True)

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Org_user, Client, Schedule, Client_schedule], safe=True)
	print("Connected to the DB and ready to rumble")
	DATABASE.close()