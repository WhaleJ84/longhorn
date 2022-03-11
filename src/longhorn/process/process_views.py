"""
Contains all the routes (views) needed for the process blueprint.
Things such as functions and forms should be in separate files.
"""
from flask import current_app as app
from flask import render_template
from pandas import read_csv

from . import process


@process.route("/processes", methods=["GET"])
def view_processes():
    """
    Dynamically generates a HTML page using the data from PROCESS_FILE.
    """
    return render_template(
        "processes.html",
        data=read_csv(
            app.config["PROCESS_FILE"]
        ).to_html(index=False, classes=['table', 'table--lined', 'table--selectable'])
    )
