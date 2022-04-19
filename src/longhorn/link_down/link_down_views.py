"""
Contains all the routes (views) needed for the link_down blueprint.
Things such as functions and forms should be in separate files.
"""
from flask import current_app as app
from flask import g, request

from src.longhorn.link_down.link_down_functions import build_response_data
from src.longhorn.process.process_functions import check_sessions
from src.longhorn.third_party.source_of_truth.netbox.netbox_functions import Netbox
from src.longhorn.third_party.service_management.faveo.faveo_functions import Faveo
from . import link_down


@link_down.route("/", methods=["POST"])
def runbook():
    """
    The route that triggers all the necessary actions to handle when a link goes down.
    """
    response = build_response_data(request.json)
    response.update({"status": 200, "message": "NO MESSAGE SET"})

    # Checking if there is already a request in the queue
    current_process = check_sessions(
        request.json["event_text"], app.config["PROCESS_FILE"]
    )
    g.process_id = current_process.process_id  # pylint: disable=assigning-non-slot
    if current_process.is_duplicate:
        message = "Duplicate response"
        app.logger.info(
            f"{g.process_id}\tduplicate response: {current_process.event_text} "
        )
        response.update({"status": 208, "message": message})
        return response, int(response["status"])

    try:
        netbox = Netbox(current_process.side_a, current_process.side_z)

        if netbox.circuit.status.label != "Active":
            message = f"circuit {netbox.circuit} is in {netbox.circuit.status} state"
            app.logger.info(f"{g.process_id}\t{message}")
            response.update({"message": message})
            return response, int(response["status"])
    except AttributeError:
        message = f"Connection error to {app.config['NETBOX_URL']}"
        app.logger.error(f"{g.process_id}\t{message}")
        response.update({"status": 503, "message": message})
        return response, int(response["status"])

    incidents = netbox.check_journal_entries()
    faveo = Faveo()
    existing_tickets = faveo.check_existing_tickets(incidents)

    if len(existing_tickets) >= 1:
        message = f"Existing open tickets: {existing_tickets}"
        app.logger.info(f"{g.process_id}\t{message}")
        response.update({"message": message})
    else:
        ticket_number = faveo.create_ticket(
            request.json["event_text"], netbox.generate_incident_template(request.json["event_text"])
        )
        response.update({"status": 201, "ticket": ticket_number})

    return response, int(response["status"])
