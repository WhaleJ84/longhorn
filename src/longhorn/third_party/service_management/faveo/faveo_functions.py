from faveo_handler import FaveoHandler
from flask import current_app as app


def check_existing_tickets(ticket_numbers: list):
    faveo = FaveoHandler(app.config["FAVEO_URL"])
    faveo.authenticate(app.config["FAVEO_USERNAME"], app.config["FAVEO_PASSWORD"])
    tickets = faveo.get_tickets()["data"]
    matching_tickets = []
    for ticket in tickets:
        for number in ticket_numbers:
            if ticket["ticket_number"] == number and ticket["status"] == 1:
                matching_tickets.append(ticket["ticket_number"])
    return matching_tickets
