from test import LonghornTestCase
from src.longhorn.link_down.link_down_functions import *


class BuildResponseDataTestCase(LonghornTestCase):
    def test_build_response_data_returns_expected_values(self):
        self.assertEqual(
            build_response_data(self.data),
            {
                "causing_ci": "lon-edge-gw1.example.com",
                "event_text": "LINK DOWN | TRANSIT-LON<>CAR | A3",
                "event_url": "https://example.com",
                "timestamp": "2021-10-15 23:20:01",
            },
        )

    def test_build_response_data_returns_relevant_values(self):
        self.data = {
            "causing_ci": "lon-edge-gw1.example.com",
            "event_text": "LINK DOWN | LON<>CAR | A3",
            "event_url": "https://example.com",
            "alphabet": "abcdefghijklmnopqrstuvwxyz",
        }
        self.assertEqual(
            build_response_data(self.data),
            {
                "causing_ci": "lon-edge-gw1.example.com",
                "event_text": "LINK DOWN | LON<>CAR | A3",
                "event_url": "https://example.com",
            },
        )
