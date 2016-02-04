import os


class Config(object):
    NOTIFY_ADMIN_URL = os.getenv('NOTIFY_ADMIN_URL', "http://localhost:6012")
    TWILIO_TEST_NUMBER = os.getenv('TWILIO_TEST_NUMBER', '')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    FUNCTION_TEST_EMAIL = os.getenv('FUNCTIONAL_TEST_EMAIL', '')
    FUNCTIONAL_TEST_PASSWORD = os.getenv('FUNCTIONAL_TEST_PASSWORD', '')

