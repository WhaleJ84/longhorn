from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import Process
from test import LonghornTestCase


class ProcessFunctionsTestCase(LonghornTestCase):
    def setUp(self) -> None:
        self.event_text = "LINK DOWN | TRANSIT-LON<>CAR | A3"
        self.process = Process(
            self.event_text,
            TestingConfig.PROCESS_FILE,
            TestingConfig.PROCESS_TTL,
            _ut=True
        )
