import flask.app

from src.manage import create_app
from test import LonghornTestCase


class LonghornManage(LonghornTestCase):
    def test_manage_creates_test_app(self):
        with self.assertLogs('src.longhorn') as logger:
            self.create_app()
        self.assertEqual(
            logger.output,
            [
                'INFO:src.longhorn:Running in: test mode'
            ]
        )

    def test_manage_defaults_to_dev_app(self):
        with self.assertLogs('src.longhorn') as logger:
            self.create_app("")
        self.assertEqual(
            logger.output,
            [
                "WARNING:src.longhorn:`LONGHORN_ENV' not found. Defaulting to Development environment",
                "WARNING:src.longhorn:No authorization tokens detected. Defaulting to: dGhpc19pc19pbnNlY3VyZQ=="
            ]
        )

    def test_manage_returns_flask_app(self):
        self.assertEqual(
            type(create_app()),
            flask.app.Flask
        )
