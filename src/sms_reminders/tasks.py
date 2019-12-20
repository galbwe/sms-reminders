import os

from celery import Celery
from twilio.rest import Client


ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

app = Celery('tasks', broker="amqp://rabbitmq:rabbitmq@localhost:5672")

@app.task
def send_sms(to, from_, message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        from_=from_,
        to=to,
        body=message
    )
