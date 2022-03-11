"""
Contains all the routes (views) needed for the link_down blueprint.
Things such as functions and forms should be in separate files.
"""
from flask import request

from src.longhorn.link_down.link_down_functions import build_response_data
from . import link_down


@link_down.route("/", methods=["POST"])
def runbook():
    """
    The route that triggers all the necessary actions to handle when a link goes down.
    """
    response = build_response_data(request.json)
    response.update({"status": 200})
    return response, int(response["status"])
