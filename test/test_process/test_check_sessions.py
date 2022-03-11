from . import ProcessFunctionsTestCase
from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import check_sessions, Process


class CheckSessionsTestCase(ProcessFunctionsTestCase):
    def test_check_sessions_doesnt_create_process_for_duplicate(self):
        csv_file = 'test/test_process/var/cache/test_processes.csv'
        process = Process(self.event_text, csv_file, TestingConfig.PROCESS_TTL)
        process.create_process()
        duplicate_process = check_sessions(self.event_text, csv_file)
        self.assertTrue(duplicate_process.is_duplicate)
        process.delete_process()
