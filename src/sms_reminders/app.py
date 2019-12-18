import os
from uuid import uuid4

from flask import Flask, request, jsonify
from twilio.rest import Client

ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

app = Flask(__name__)

reminders = []

@app.route('/reminders', methods=['GET'])
def get_all_reminders():
    return jsonify(reminders)

@app.route('/reminders', methods=['POST'])
def create_reminder():
    global reminders
    reminder = request.get_json()
    reminder['id'] = str(uuid4())
    reminders.append(reminder)
    return "success", 200

@app.route('/reminders/<id>', methods=['GET'])
def get_reminder_by_id(id):
    for reminder in reminders:
        if reminder['id'] == id:
            return jsonify(reminder)
    return None

@app.route('/reminders/<id>', methods=['PUT'])
def edit_reminder(id):
    global reminders
    new_reminder = request.get_json()
    for i, reminder in enumerate(reminders):
        if reminder['id'] == id:
            new_reminder['id'] = id
            reminders[i] = new_reminder
            return jsonify(new_reminder)
    return None

@app.route('/reminders/<id>', methods=['DELETE'])
def delete_reminder(id):
    global reminders
    reminders = filter(lambda r: r['id'] != id, reminders)

@app.route('/reminders/<id>/send', methods=['GET'])
def send_reminder(id):
    for reminder in reminders:
        if reminder['id'] == id:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                from_=reminder['from'],
                to=reminder['to'],
                body=reminder['message']
            )
            return "reminder sent", 200
    return "reminder not found", 400
