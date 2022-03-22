"""
Contains all the functions needed for the link_down blueprint.
Things such as routes and forms should be in separate files.
"""
from json import loads

from flask import current_app as app
from flask import request

from src.longhorn.authentication.authentication_functions import auth
from src.longhorn.email.email_functions import send_alert_transport_via_email
from . import link_down


def build_response_data(data: dict) -> dict:
    """
    Takes the request data and extracts the relevant matches for the required data.
    When all expected parameters are received, they are returned in a sorted dictionary.
    When unexpected parameters are received, they are omitted from the returned dictionary.

    :param data: Raw request data in dict or JSON format
    :return:  Relevant request data in alphabetical order
    """
    response = {}
    expected_parameters = ["causing_ci", "event_text", "event_url", "timestamp"]

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


@link_down.after_request
def call_alert_transport(response):
    """
    Alert transports are methods that notify engineers of actions performed.
    This method calls the transport specified by app.config["ALERT_TRANSPORT"]

    :param response: The response object returned from Flask
    """
    data = loads(response.get_data().decode())

    if app.config["ALERT_TRANSPORT"] == "email":
        send_alert_transport_via_email(data)
    return response
