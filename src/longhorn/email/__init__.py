"""
Initialises the email blueprint while building the app.
"""
from flask import Blueprint

email = Blueprint("email", __name__)

# imports have to remain down here to prevent circular import errors
from . import email_functions
