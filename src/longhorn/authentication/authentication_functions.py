"""
Contains all the functions needed for the authentication blueprint.
Things such as routes and forms should be in separate files.
"""
from flask import request
from flask import current_app as app
from flask_httpauth import (
    HTTPTokenAuth,
)  # https://flask-httpauth.readthedocs.io/en/latest/index.html

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token: str):
    """
    Takes the request header value from 'Authorization' and verifies the latter half is in the system.
    Once authenticated, the user is stored inside `auth.current_user()`.

    :param token: A string value used to authenticate the user against the system
    :return: The currently authenticated user
    """
    tokens = dict(app.config["AUTH_TOKENS"])

    if app.config["LOGIN_DISABLED"]:
        return "login-disabled"

    if token in tokens:
        app.logger.debug(f"Authorized request from: {tokens[token]}")
        return tokens[token]
    return None


@auth.error_handler
def auth_error(status: int, data: dict = None):
    """
    Provides the user with an appropriate error response depending on the fault.

    :param status: The integer value of the HTTP response code
    :param data: The request data from flask
    :return: A dictionary response containing the HTTP response code and failure message
    """
    response = {
        "status": status,
    }

    if not data:
        data = request.json

    # this try/except exists to allow unit-testing of this method as tests aren't run the same as in prod.
    # if no event_text is sent, it will be caught in a later step when verifying the request body.
    try:
        response.update({"event_text": data["event_text"]})
    except KeyError:
        pass
    except TypeError:
        pass

    try:
        response.update({"event_url": data["event_url"]})
    except KeyError:
        pass
    except TypeError:
        pass

    if status == 401:
        message = "Unauthorized request"
        app.logger.warning(message)
        response.update({"message": message})

    return response
