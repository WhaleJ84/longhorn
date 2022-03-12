"""
Contains all the functions needed for the link_down blueprint.
Things such as routes and forms should be in separate files.
"""
from flask import current_app as app
from flask import request

from src.longhorn.authentication.authentication_functions import auth
from . import link_down


def build_response_data(data: dict) -> dict:
    """
    Takes the request data and extracts the relevant matches for the required data.

    When all expected parameters are recieved, they are returned in a sorted dictionary.

    >>> build_response_data({
    ... "event_url": "https://example.com",
    ... "timestamp": "2021-10-15 23:20:01",
    ... "causing_ci": "hostname.example.com"
    ... })
    {'causing_ci': 'hostname.example.com', 'event_url': 'https://example.com', 'timestamp': '2021-10-15 23:20:01'}


    When unexpected parameters are recieved, they are omitted from the returned dictionary.

    >>> build_response_data({"alphabet": "abcdefghijklmnopqrstuvwxyz",
    ... "event_url": "https://example.com", "timestamp": "2021-10-15 23:20:01"})
    {'event_url': 'https://example.com', 'timestamp': '2021-10-15 23:20:01'}

    :param data: Raw request data in dict or JSON format
    :return:  Relevant request data in alphabetical order
    """
    response = {}
    expected_parameters = [
        "causing_ci", "event_text", "event_url", "timestamp"
    ]

    for parameter in expected_parameters:
        if parameter in data:
            response.update({f"{parameter}": data[parameter]})
    return response


@link_down.before_request
@auth.login_required
def verify_data():
    """
    Ensures the JSON values received in the request body includes all required data.
    For any missed value, a list will be returned containing the remaining requirements.
    """
    missing_data = ["causing_ci", "event_text", "timestamp"]

    for entry in dict(request.json):
        if entry in missing_data:
            missing_data.remove(entry)

    if missing_data:
        response = build_response_data(dict(request.json))
        message = f"Missing: {missing_data} from required data"
        response.update({"status": 400, "message": message})
        app.logger.warning(f"{auth.current_user()}: {message}")
        return response, response["status"]
    return None
