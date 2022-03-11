from . import ProcessFunctionsTestCase
from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import Process


class DeleteProcessTestCase(ProcessFunctionsTestCase):
    def test_delete_process_deletes_process(self):
        test_process = Process(
            self.event_text,
            TestingConfig.PROCESS_FILE,
            TestingConfig.PROCESS_TTL,
            _ut=True,
        )
        test_process.create_process()
        test_process.delete_process()
        with open(TestingConfig.PROCESS_FILE, "rt") as process_file:
            self.assertNotIn(test_process.process_id, process_file.read())
