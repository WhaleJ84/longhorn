from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import Process
from test import LonghornTestCase


class TestProcessFunctions(LonghornTestCase):
    def setUp(self) -> None:
        self.event_text = self.data["event_text"]
        self.process_file = TestingConfig.PROCESS_FILE
        self.process = Process(self.event_text, self.process_file, TestingConfig.PROCESS_TTL)
