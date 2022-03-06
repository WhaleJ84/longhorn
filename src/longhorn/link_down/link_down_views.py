"""
Contains all the routes (views) needed for the link_down blueprint.
Things such as functions and forms should be in separate files.
"""
from flask import current_app as app
from flask import request

from . import link_down


@link_down.route("/", methods=["POST"])
def runbook():
    """
    The route that triggers all the necessary actions to handle when a link goes down.
    """
    app.logger.info(f"request: {request.data}")
    return {'status': 200}
