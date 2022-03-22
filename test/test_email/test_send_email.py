from flask_mail import Message

from src.longhorn.email.email_functions import send_email
from test import LonghornTestCase


class SendEmailTestCase(LonghornTestCase):
    def test_send_email_notifies_on_success(self):
        message = Message(
            "Unit test subject",
            ["unittest-recipient@example.com"],
            "This is a unit test email.",
            sender="unittest-sender@example.com"
        )
        self.assertEqual(
            send_email(message),
            {
                "cc": [],
                "message": "This is a unit test email.",
                "outbox": 1,
                "recipients": ["unittest-recipient@example.com"],
                "sender": "unittest-sender@example.com",
                "subject": "Unit test subject",
            },
        )
