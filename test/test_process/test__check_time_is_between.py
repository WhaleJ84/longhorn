from datetime import datetime

from . import ProcessFunctionsTestCase
from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import Process


class CheckTimeIsBetweenTestCase(ProcessFunctionsTestCase):
    def setUp(self) -> None:
        self.event_text = "LINK DOWN | TRANSIT-LON<>CAR | A3"
        self.process_file = TestingConfig.PROCESS_FILE
        self.hold_start = datetime(1970, 1, 1, 0, 6, 1, 123456)
        self.process = Process(
            self.event_text,
            self.process_file,
            TestingConfig.PROCESS_TTL,
            self.hold_start,
            _ut=True,
        )

    def test_check_time_is_between_returns_true_when_time_is_in_range(self):
        self.assertTrue(
            self.process._check_time_is_between(
                datetime(1970, 1, 1, 0, 5, 1, 123456),
                datetime(1970, 1, 1, 0, 10, 1, 123456),
            )
        )

    def test_check_time_is_between_returns_false_when_time_is_after_range(self):
        self.assertFalse(
            self.process._check_time_is_between(
                datetime(1970, 1, 1, 0, 10, 1, 123456),
                datetime(1970, 1, 1, 0, 15, 1, 123456),
            )
        )

    def test_check_time_is_between_returns_false_when_time_is_before_range(self):
        self.assertFalse(
            self.process._check_time_is_between(
                datetime(1970, 1, 1, 0, 0, 1, 123456),
                datetime(1970, 1, 1, 0, 5, 1, 123456),
            )
        )

    def test_check_time_is_between_returns_false_when_end_is_before_start(self):
        self.assertFalse(
            self.process._check_time_is_between(
                datetime(1970, 1, 1, 0, 5, 1, 123456),
                datetime(1970, 1, 1, 0, 0, 1, 123456),
            )
        )
