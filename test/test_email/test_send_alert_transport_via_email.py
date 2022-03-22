from flask_mail import Message

from src.longhorn.email.email_functions import send_email
from test import LonghornTestCase


class SendEmailTestCase(LonghornTestCase):
    def test_send_email_notifies_on_success(self):
        pass
