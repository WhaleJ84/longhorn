"""
Initialises the process blueprint while building the app.
"""
from flask import Blueprint

process = Blueprint("process", __name__)

# imports have to remain down here to prevent circular import errors
from . import process_functions, process_views
