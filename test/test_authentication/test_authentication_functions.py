from src.longhorn.authentication.authentication_functions import app, verify_token
from test import LonghornTestCase


class VerifyTokenTestCase(LonghornTestCase):
    def test_verify_token_returns_none_on_bad_token(self):
        self.headers["Authorization"] = "Bearer WRONG_TOKEN"
        self.assertIsNone(verify_token(self.headers["Authorization"].split()[1]))

    def test_verify_token_returns_login_disabled_on_variable_set(self):
        app.config["LOGIN_DISABLED"] = True
        self.assertEqual("login-disabled", verify_token(self.headers["Authorization"]))

    def test_verify_token_returns_user_dict_on_good_token(self):
        with app.app_context():
            self.assertEqual("unit-test", verify_token(self.headers["Authorization"].split()[1]))
