import os

from celery import Celery

from celery.schedules import crontab
from twilio.rest import Client


ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

app = Celery('tasks', broker="amqp://rabbitmq:rabbitmq@localhost:5672",
             backend="redis://localhost:6379")


# task that periodically checks a database for messages that need to be sent
# @app.task
# def check_for_messages():

@app.task
def send_sms(to, from_, message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        from_=from_,
        to=to,
        body=message
    )
