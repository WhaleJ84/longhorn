from . import ProcessFunctionsTestCase
from src.longhorn.config import TestingConfig
from src.longhorn.process.process_functions import Process


class GetDuplicateRequestsTestCase(ProcessFunctionsTestCase):
    def test_get_duplicate_requests_returns_list_of_similar_processes_regardless_of_time(self):
        process_file = "test/test_process/var/cache/test_static_processes.csv"
        test_process = Process(self.event_text, process_file, TestingConfig.PROCESS_TTL, _ut=True)
        duplicate_requests = test_process._get_duplicate_requests(process_file)
        self.assertEqual(
            duplicate_requests,
            [
                [
                    "8895307d-3a69-4c33-b1c4-abd43d3cbd1e",
                    "TRANSIT",
                    "LON",
                    "CAR",
                    "2021-05-14 13:28:31.021898",
                    "2021-05-14 13:33:31.021898",
                ],
                [
                    "e8891fcc-134d-474d-8f2c-98ca515e74de",
                    "TRANSIT",
                    "LON",
                    "CAR",
                    "2021-05-14 13:57:24.674659",
                    "2021-05-14 14:02:24.674659",
                ],
            ],
        )
