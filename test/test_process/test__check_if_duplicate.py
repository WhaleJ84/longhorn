from datetime import datetime

from . import ProcessFunctionsTestCase
from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import Process


class CheckIfDuplicateTestCase(ProcessFunctionsTestCase):
    def test_check_if_duplicate_returns_true_if_duplicate_is_in_range_of_other(self):
        self.new_process = Process(
            self.event_text,
            TestingConfig.PROCESS_FILE,
            TestingConfig.PROCESS_TTL,
            datetime(2021, 5, 14, 13, 59, 59, 123456),
            _ut=True,
        )
        self.assertTrue(
            self.new_process._check_if_duplicate(
                [
                    [
                        "1",
                        "TRANSIT",
                        "LON",
                        "CAR",
                        "2021-05-14 13:57:24.674659",
                        "2021-05-14 14:02:24.674659",
                    ]
                ]
            )
        )

    def test_check_if_duplicate_returns_false_if_duplicate_is_not_in_range_of_other(self):
        self.assertFalse(
            self.process._check_if_duplicate(
                [
                    [
                        "1",
                        "TRANSIT",
                        "LON",
                        "CAR",
                        "2021-05-14 13:28:31.021898",
                        "2021-05-14 13:33:31.021898",
                    ]
                ]
            )
        )
