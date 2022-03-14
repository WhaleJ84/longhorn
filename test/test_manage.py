import flask.app

from src.manage import create_app
from test import LonghornTestCase


class TestManage(LonghornTestCase):
    def test_manage_creates_test_app(self):
        with self.assertLogs("src.longhorn") as logger:
            self.create_app()
        self.assertEqual(logger.output, ["INFO:src.longhorn:Running in: test mode"])

    def test_manage_defaults_to_dev_app(self):
        with self.assertLogs("src.longhorn") as logger:
            self.create_app("")
        self.assertIn(
            "WARNING:src.longhorn:`LONGHORN_ENV' not found. Defaulting to Development environment",
            logger.output,
        )

    def test_manage_has_auth_tokens_defaulted_on_none(self):
        self.app = self.create_app("broken")
        self.assertEqual(
            {self.app.config["DEFAULT_TOKEN"]: "unknown-user"},
            self.app.config["AUTH_TOKENS"]
        )

    def test_manage_returns_flask_app(self):
        self.assertEqual(type(create_app()), flask.app.Flask)
