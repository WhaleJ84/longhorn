"""
Initialises the link_down blueprint while building the app.
"""
from flask import Blueprint

link_down = Blueprint("link_down", __name__)

# imports have to remain down here to prevent circular import errors
from . import link_down_views
