from os import getenv

from flask_testing import (
    TestCase,
)  # https://flask.palletsprojects.com/en/1.1.x/testing/

from src.longhorn import create_app


class LonghornTestCase(TestCase):
    def create_app(self, env: str = "test"):
        return create_app(env)

    def setUp(self) -> None:
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer test",
        }
        self.data = {
            "causing_ci": "lon-edge-gw1.example.com",
            "event_text": "LINK DOWN | LON<>CAR | A3",
            "event_url": "https://example.com",
            "timestamp": "2021-10-15 23:20:01"
        }
        self.client = self.app.test_client()
