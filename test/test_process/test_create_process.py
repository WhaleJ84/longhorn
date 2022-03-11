from . import ProcessFunctionsTestCase
from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import Process


class CreateProcessTestCase(ProcessFunctionsTestCase):
    def test_create_process_creates_process(self):
        test_process = Process(
            self.event_text,
            TestingConfig.PROCESS_FILE,
            TestingConfig.PROCESS_TTL,
            _ut=True,
        )
        test_process.create_process()
        with open(TestingConfig.PROCESS_FILE, "rt") as process_file:
            self.assertIn(test_process.process_id, process_file.read())
        test_process.delete_process()
