from flask import url_for

from test import LonghornTestCase


class TestProcessViewsTestCase(LonghornTestCase):
    def test_view_processes_returns_200_on_get_request(self):
        self.assert200(self.client.get(url_for("process.view_processes")))
