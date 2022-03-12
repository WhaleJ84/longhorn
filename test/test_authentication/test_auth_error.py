from src.longhorn.authentication.authentication_functions import auth_error
from test import LonghornTestCase


class AuthErrorTestCase(LonghornTestCase):
    def test_auth_error_returns_401_on_bad_auth_token(self):
        self.assertEqual({"message": "Unauthorized request", "status": 401}, auth_error(401).json)
