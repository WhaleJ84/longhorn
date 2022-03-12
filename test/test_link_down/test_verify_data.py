from flask import url_for

from src.longhorn.link_down.link_down_functions import app, verify_data
from test import LonghornTestCase


class VerifyDataTestCase(LonghornTestCase):
    def test_verify_data_returns_none_on_good_json(self):
        with app.test_request_context(
            url_for("link_down.runbook"),
            method="POST",
            json=self.data,
            headers=self.headers,
        ):
            self.assertIsNone(verify_data())

    def test_verify_data_returns_400_status_on_bad_json(self):
        self.data.pop("event_text")
        with app.test_request_context(
            url_for("link_down.runbook"),
            method="POST",
            json=self.data,
            headers=self.headers,
        ):
            response = verify_data()
            self.assertEqual(400, response[1])

    def test_verify_data_returns_informative_message_on_bad_json(self):
        self.data.pop("event_text")
        with app.test_request_context(
            url_for("link_down.runbook"),
            method="POST",
            json=self.data,
            headers=self.headers,
        ):
            response = verify_data()
            self.assertEqual(
                "Missing: ['event_text'] from required data", response[0]["message"]
            )
