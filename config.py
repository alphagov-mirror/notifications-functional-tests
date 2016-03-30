import os


class Config(object):
    ENVIRONMENT = os.environ['ENVIRONMENT']
    NOTIFY_ADMIN_URL = os.environ['NOTIFY_ADMIN_URL']
    TWILIO_TEST_NUMBER = os.environ['TWILIO_TEST_NUMBER']
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    FUNCTIONAL_TEST_EMAIL = os.environ['FUNCTIONAL_TEST_EMAIL']
    FUNCTIONAL_TEST_PASSWORD = os.environ['FUNCTIONAL_TEST_PASSWORD']
    FUNCTIONAL_TEMPLATE_ID = os.environ['TEMPLATE_ID']
    FUNCTIONAL_SERVICE_ID = os.environ['SERVICE_ID']
    EMAIL_FOLDER = 'notify'
    REGISTRATION_EMAIL = 'registration'
    EMAIL_TRIES = 10
    EMAIL_DELAY = 5
