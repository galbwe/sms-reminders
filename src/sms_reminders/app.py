from uuid import uuid4
import os

from configparser import ConfigParser
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID

from tasks import send_sms

app = Flask(__name__)

# database configuration
def get_database_url(filepath):
    config = ConfigParser()
    config.read(filepath)
    user = config['flask']['database_user']
    pw = config['flask']['database_password']
    url = config['flask']['database_host']
    db = config['flask']['database']
    return f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'


config_file = os.environ.get('CONFIG_FILE') or './config.ini'
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url(config_file)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# database models
class Reminder(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    to = db.Column(db.String(12), nullable=False) # +18459873492
    from_ = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime(), nullable=False)
    is_recurring = db.Column(db.Boolean, default=False)

class ReminderSchema(ma.ModelSchema):
    class Meta:
        model = Reminder

@app.route('/reminders', methods=['GET'])
def get_all_reminders():
    reminders = Reminder.query.all()
    reminder_schema = ReminderSchema(many=True)
    return jsonify(reminder_schema.dump(reminders)), 200

@app.route('/reminders', methods=['POST'])
def create_reminder():
    reminder_schema = ReminderSchema()
    reminder = reminder_schema.load(request.get_json())
    db.session.add(reminder)
    db.session.commit()
    return jsonify(reminder_schema.dump(reminder)), 200

@app.route('/reminders/<id>', methods=['GET'])
def get_reminder_by_id(id):
    reminder = Reminder.query.filter_by(uuid=id).first()
    return jsonify(ReminderSchema().dump(reminder)), 200

@app.route('/reminders/<id>', methods=['PUT'])
def edit_reminder(id):
    new_reminder = request.get_json()
    new_reminder['uuid'] = id
    new_reminder = ReminderSchema().load(new_reminder)
    reminder = Reminder.query.filter_by(uuid=id).first()
    reminder.to = new_reminder.to
    reminder.from_ = new_reminder.from_
    reminder.message = new_reminder.message
    reminder.time = new_reminder.time
    reminder.is_recurring = new_reminder.is_recurring
    db.session.commit(reminder)
    return jsonify(ReminderSchema().dump(reminder)), 200

@app.route('/reminders/<id>', methods=['DELETE'])
def delete_reminder(id):
    reminder = Reminder.query.filter_by(uuid=id).first()
    db.session.delete(reminder)
    return jsonify(ReminderSchema().dump(reminder)), 200

@app.route('/reminders/<id>/send', methods=['GET'])
def send_reminder(id):
    reminder = Reminder.query.filter_by(uuid=id).first()
    send_sms.delay(reminder.to, reminder.from_, reminder.message)
    return "reminder sent", 200
