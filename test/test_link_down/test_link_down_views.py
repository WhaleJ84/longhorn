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
