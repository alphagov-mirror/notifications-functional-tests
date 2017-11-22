from config import Config
from tests.pages import (
    SignInPage,
    DashboardPage,
    SendEmailTemplatePage,
    EditEmailTemplatePage,
    SendSmsTemplatePage,
    EditSmsTemplatePage,
    ApiKeyPage,
    ShowTemplatesPage,
    SelectTemplatePage
)

from tests.test_utils import do_verify, do_email_auth_verify


def sign_in(driver, test_profile, seeded=False):
    _sign_in(driver, test_profile, 'seeded' if seeded else 'normal')
    do_verify(driver, test_profile)


def sign_in_email_auth(driver, test_profile):
    _sign_in(driver, test_profile, 'email_auth')
    assert driver.current_url == Config.NOTIFY_ADMIN_URL + '/two-factor-email-sent'
    do_email_auth_verify(driver, test_profile)


def _sign_in(driver, test_profile, account_type):
    sign_in_page = SignInPage(driver)
    sign_in_page.get()
    assert sign_in_page.is_current()
    email, password = _get_email_and_password(test_profile, account_type=account_type)
    sign_in_page.login(email, password)


def _get_email_and_password(profile, account_type):
    if account_type == 'normal':
        return profile.email, profile.password
    elif account_type == 'seeded':
        return profile.notify_research_service_email, profile.notify_research_service_password
    elif account_type == 'email_auth':
        return profile.notify_research_service_email_auth_account, profile.notify_research_service_password
    raise Exception('unknown account_type {}'.format(account_type))


def get_service_templates_and_api_key_for_tests(driver, test_profile):

    dashboard_page = DashboardPage(driver)
    dashboard_page.click_templates()
    service_id = dashboard_page.get_service_id()

    show_templates_page = ShowTemplatesPage(driver)
    show_templates_page.click_add_new_template()

    select_template_page = SelectTemplatePage(driver)
    select_template_page.select_email()
    select_template_page.click_continue()

    new_email_template_page = EditEmailTemplatePage(driver)
    new_email_template_page.create_template()

    email_template_page = SendEmailTemplatePage(driver)
    email_template_page.click_edit_template()

    edit_email_template_page = EditEmailTemplatePage(driver)
    email_template_id = edit_email_template_page.get_id()

    dashboard_page = DashboardPage(driver)
    dashboard_page.go_to_dashboard_for_service()
    dashboard_page.click_templates()

    show_templates_page = ShowTemplatesPage(driver)
    show_templates_page.click_add_new_template()

    select_template_page = SelectTemplatePage(driver)
    select_template_page.select_text_message()
    select_template_page.click_continue()

    new_sms_template = EditSmsTemplatePage(driver)
    new_sms_template.create_template()

    sms_template_page = SendSmsTemplatePage(driver)
    sms_template_page.click_edit_template()

    edit_sms_template = EditSmsTemplatePage(driver)
    sms_template_id = edit_sms_template.get_id()

    dashboard_page = DashboardPage(driver)
    dashboard_page.go_to_dashboard_for_service()
    dashboard_page.click_api_keys_link()

    api_key_page = ApiKeyPage(driver)
    api_key_page.click_keys_link()
    api_key_page.click_create_key()

    api_key_page.click_key_type_radio(key_type='team')
    api_key_page.enter_key_name(key_type='team')

    api_key_page.click_continue()
    api_key = api_key_page.get_api_key()

    test_profile.service_id = service_id
    test_profile.jenkins_build_email_template_id = email_template_id
    test_profile.jenkins_build_sms_template_id = sms_template_id
    test_profile.api_key = api_key

    return {'service_id': service_id, 'api_key': api_key}
