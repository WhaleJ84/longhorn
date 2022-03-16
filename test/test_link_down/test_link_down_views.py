from flask import url_for

from test import LonghornTestCase


class LinkDownViewsTestCase(LonghornTestCase):
    def test_runbook_returns_200_on_post_request(self):
        self.assert200(
            self.client.post(
                url_for("link_down.runbook"), json=self.data, headers=self.headers
            )
        )

    def test_runbook_returns_208_on_duplicate_response(self):
        self.client.post(
            url_for("link_down.runbook"),
            json=self.data,
            headers=self.headers,
        )
        response = self.client.post(
            url_for("link_down.runbook"),
            json=self.data,
            headers=self.headers,
        )
        self.assertEqual(response.json["status"], 208)

    def test_runbook_returns_503_on_unreachable_source_of_truth(self):
        with self.app.app_context():
            self.app.config["NETBOX_URL"] = "https://netbox.example.com"
        self.data["event_text"] = "LINK DOWN | TRANSIT-CAR<>DUB | B3"
        self.assertStatus(
            self.client.post(url_for('link_down.runbook'), json=self.data, headers=self.headers),
            503
        )
