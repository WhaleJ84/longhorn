"""
Initialises the authentication blueprint while building the app.
"""
from flask import Blueprint

authentication = Blueprint("authentication", __name__)

# imports have to remain down here to prevent circular import errors
from . import authentication_functions
