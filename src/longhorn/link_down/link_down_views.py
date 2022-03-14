"""
Contains all the routes (views) needed for the link_down blueprint.
Things such as functions and forms should be in separate files.
"""
from flask import current_app as app
from flask import request

from src.longhorn.link_down.link_down_functions import build_response_data
from src.longhorn.process.process_functions import check_sessions
from src.longhorn.third_party.source_of_truth.netbox.netbox_functions import Netbox
from . import link_down


@link_down.route("/", methods=["POST"])
def runbook():
    """
    The route that triggers all the necessary actions to handle when a link goes down.
    """
    response = build_response_data(request.json)
    response.update({"status": 200})

    # Checking if there is already a request in the queue
    current_process = check_sessions(
        request.json["event_text"], app.config["PROCESS_FILE"]
    )
    if current_process.is_duplicate:
        message = "Duplicate response"
        app.logger.info(
            f"{current_process.process_id}\tduplicate response: {current_process.event_text} "
        )
        response.update({"status": 208, "message": message})
        return response, int(response["status"])

    netbox = Netbox()

    if netbox.circuit.status.label != 'Active':
        message = f'circuit {netbox.circuit} is in {netbox.circuit.status} state'
        app.logger.info(
           f"{current_process.process_id}\t{message}"
        )

    return response, int(response["status"])
