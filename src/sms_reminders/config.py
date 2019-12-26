import os

from configparser import ConfigParser


config_file = os.environ.get('CONFIG_FILE') or './config.ini'
# database configuration
def get_database_url(filepath):
    config = ConfigParser()
    config.read(filepath)
    user = config['flask']['database_user']
    pw = config['flask']['database_password']
    url = config['flask']['database_host']
    db = config['flask']['database']
    return f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'


def get_twilio_account_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    account_sid = config['twilio']['account_sid']
    auth_token = config['twilio']['auth_token']
    return account_sid, auth_token
