from shutil import copy

from . import ProcessFunctionsTestCase
from src.longhorn.process.process_functions import delete_process_entries


class DeleteProcessEntriesTestCase(ProcessFunctionsTestCase):
    def test_delete_process_entries_deletes_process_entries(self):
        # make copy of original file
        test_file = "test/test_process/var/cache/test_deleting_process_entries.csv"
        copy(
            "test/test_process/var/cache/test_static_processes.csv",
            test_file,
        )
        delete_process_entries(test_file)
        with open(test_file, "rt") as process_file:
            self.assertEqual(
                process_file.read(),
                "ID,Circuit Type,Side A,Side Z,Time Logged,Hold Expires\n",
            )
