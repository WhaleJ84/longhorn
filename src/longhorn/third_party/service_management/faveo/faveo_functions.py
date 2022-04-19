from faveo_handler import FaveoHandler
from flask import current_app as app


class Faveo:
    def __init__(self):
        self.api = FaveoHandler(app.config["FAVEO_URL"])
        self.api.authenticate(app.config["FAVEO_USERNAME"], app.config["FAVEO_PASSWORD"])
        response = self.api.get_authenticated_user()
        self.email = response["user"]["email"]
        self.first_name = response["user"]["first_name"]
        self.last_name = response["user"]["last_name"]
        self.ticket_id = None
        self.ticket_id_url = None

    def check_existing_tickets(self, logged_tickets: list):
        tickets = self.api.get_tickets()["data"]
        matching_tickets = []
        for ticket in tickets:
            for url in logged_tickets:
                if int(ticket["id"]) == int(str(url).split("/")[-1]) and ticket["status"] == 1:
                    matching_tickets.append({"ticket_number": ticket["ticket_number"], "url": url})
        app.logger.info(f"Found {len(matching_tickets)} existing tickets: {matching_tickets}")
        return matching_tickets

    def create_ticket(self, subject: str, body: str):
        self.ticket_id = self.api.create_ticket(
            body=body,
            email=self.email,
            first_name=self.first_name,
            helptopic=1,
            last_name=self.last_name,
            priority=3,
            sla=1,
            subject=subject
        )["response"]["ticket_id"]
        self.ticket_id_url = f"{app.config['FAVEO_URL']}/thread/{self.ticket_id}"
        app.logger.info(f"Created ticket: {self.ticket_id_url}")
        return self.ticket_id
