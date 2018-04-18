import uuid
import os

import pytest


def generate_unique_email(email, uuid):
    parts = email.split('@')
    return "{}+{}@{}".format(parts[0], uuid, parts[1])


# global variable
config = {
    # static
    'notification_retry_times': 15,
    'notification_retry_interval': 5,
    'provider_retry_times': 12,
    'provider_retry_interval': 22,
    'verify_code_retry_times': 8,
    'verify_code_retry_interval': 9,
    'functional_test_service_name': 'Functional Test Service_',

    'letter_contact_data': {"address_line_1": "test", "address_line_2": "London", "postcode": "N1"},

    # notify templates
    'notify_templates': {
        'email_auth_template_id': '299726d2-dba6-42b8-8209-30e1d66ea164',
        'invitation_template_id': '4f46df42-f795-4cc4-83bb-65ca312f49cc',
        'org_invitation_template_id': '203566f0-d835-47c5-aa06-932439c86573',
        'registration_template_id': 'ece42649-22a8-4d06-b87f-d52d5d3f0a27',
        'verify_code_template_id': '36fb0730-6259-4da1-8a80-c8de22ad4246',
    }
}


urls = {
    'dev': {
        'api': 'http://localhost:6011',
        'admin': 'http://localhost:6012'
    },
    'preview': {
        'api': 'https://api.notify.works',
        'admin': 'https://www.notify.works'
    },
    'staging': {
        'api': 'https://api.staging-notify.works',
        'admin': 'https://www.staging-notify.works'
    },
    'live': {
        'api': 'https://api.notifications.service.gov.uk',
        'admin': 'https://www.notifications.service.gov.uk'
    }
}


def setup_config():
    env = os.environ['ENVIRONMENT'].lower()

    config.update({
        'notify_api_url': urls[env]['api'],
        'notify_admin_url': urls[env]['admin'],
    })

    # (dev, preview)
    if env in {'dev', 'preview'}:
        uuid_for_test_run = str(uuid.uuid4())

        config.update({
            'env': env,

            'service_name': 'Functional Test_{}'.format(uuid_for_test_run),

            'user': {
                'name': '{}_Functional Test_{}'.format(env, uuid_for_test_run),
                'email': generate_unique_email(os.environ['FUNCTIONAL_TEST_EMAIL'], uuid_for_test_run),
                'password': os.environ['FUNCTIONAL_TEST_PASSWORD'],
                'mobile': os.environ['TEST_NUMBER'],
            },

            'notify_service_api_key': os.environ['NOTIFY_SERVICE_API_KEY'],

            'service': {
                'id': os.environ['NOTIFY_RESEARCH_SERVICE_ID'],
                'name': os.environ['NOTIFY_RESEARCH_SERVICE_NAME'],

                'seeded_user': {
                    'email': os.environ['NOTIFY_RESEARCH_MODE_EMAIL'],
                    'password': os.environ['NOTIFY_RESEARCH_MODE_EMAIL_PASSWORD'],
                },
                'api_live_key': os.environ['NOTIFY_RESEARCH_SERVICE_API_KEY'],
                'api_test_key': os.environ['NOTIFY_RESEARCH_SERVICE_API_TEST_KEY'],

                # email address of seeded email auth user
                'email_auth_account': os.environ['NOTIFY_RESEARCH_SERVICE_EMAIL_AUTH_ACCOUNT'],
                'organisation_id': os.environ['NOTIFY_RESEARCH_ORGANISATION_ID'],

                'email_reply_to': os.environ['NOTIFY_RESEARCH_EMAIL_REPLY_TO'],

                'sms_sender_text': 'func tests',

                'templates': {
                    'email': os.environ['JENKINS_BUILD_EMAIL_TEMPLATE_ID'],
                    'sms': os.environ['JENKINS_BUILD_SMS_TEMPLATE_ID'],
                    'letter': os.environ['JENKINS_BUILD_LETTER_TEMPLATE_ID'],
                }
            },

            'document_download': {
                'api_host': os.environ['DOCUMENT_DOWNLOAD_API_HOST'],
                'api_key': os.environ['DOCUMENT_DOWNLOAD_API_KEY']
            }
        })
    elif env in {'staging', 'live'}:
        # staging and live run the same simple smoke tests
        config.update({
            'env': os.environ['ENVIRONMENT'],
            'name': '{} Functional Tests'.format(env),
            'user': {
                'email': os.environ['FUNCTIONAL_TEST_EMAIL'],
                'password': os.environ['FUNCTIONAL_TEST_PASSWORD'],
                'mobile': os.environ['TEST_NUMBER'],
            },

            'notify_service_api_key': os.environ['NOTIFY_SERVICE_API_KEY'],

            # this is either a live service or in research mode, depending on what tests are running
            # (provider vs functional smoke tests)
            'service': {
                'id': os.environ['SERVICE_ID'],
                'api_key': os.environ['API_KEY'],

                'templates': {
                    'email': os.environ['JENKINS_BUILD_EMAIL_TEMPLATE_ID'],
                    'sms': os.environ['JENKINS_BUILD_SMS_TEMPLATE_ID'],
                    'letter': os.environ['JENKINS_BUILD_LETTER_TEMPLATE_ID'],
                }
            }
        })
    else:
        pytest.fail('env "{}" not one of dev, preview, staging, live'.format(env))
