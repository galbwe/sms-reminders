from celery import Celery

from celery.schedules import crontab
from twilio.rest import Client

from config import config_file, get_twilio_account_config


app = Celery('tasks', broker="amqp://rabbitmq:rabbitmq@localhost:5672",
             backend="redis://localhost:6379")


# task that periodically checks a database for messages that need to be sent
# @app.task
# def check_for_messages():

# @app.task
def send_sms(to, from_, message):
    account_sid, auth_token = get_twilio_account_config(config_file)
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=from_,
        to=to,
        body=message
    )
