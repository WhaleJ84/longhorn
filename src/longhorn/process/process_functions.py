"""
Contains all the functions needed for the process blueprint.
Things such as routes and forms should be in separate files.
"""
from csv import reader, writer
from datetime import datetime, timedelta
from random import randint
from re import match, search
from threading import Timer
from uuid import uuid4

from flask import current_app as app


class Process:  # pylint: disable=too-many-instance-attributes
    """
    Builds an object out of an incoming request to enable process logging.
    """

    def __init__(
        self,
        event_text: str,
        process_file: str = "src/longhorn/var/cache/processes.csv",
        hold_delay_in_seconds: int = 300,
        hold_start: datetime = datetime.utcnow(),
        _ut: bool = False,
    ):
        """
        Builds an object out of an incoming request to enable process logging.

        :param event_text: The event_text received inside the request data
        :param process_file: The location where the CSV file is located to track processes
        :param hold_delay_in_seconds: How long in seconds any requests from the same two sides will be ignored for
        :param hold_start: The UTC datetime when the request came in
        """
        self.process_file = process_file
        self.process_id = str(uuid4())
        self.hold_delay_in_seconds = hold_delay_in_seconds
        self.event_text = event_text
        self.link_type = str()
        self.side_a = str()
        self.side_z = str()
        self._set_circuit_info()
        self.hold_start = hold_start
        self.hold_end = self.hold_start + timedelta(seconds=self.hold_delay_in_seconds)

        self.duplicate_requests = []
        self.is_duplicate = bool()
        if not _ut:
            self.duplicate_requests = self._get_duplicate_requests(self.process_file)
            self.is_duplicate = self._check_if_duplicate(self.duplicate_requests)

            if self.is_duplicate is False:
                self.create_process()
                random_time = self.hold_delay_in_seconds + randint(0, 9)  # nosec B311
                app.logger.debug(f"Keeping process alive for {random_time} seconds")
                ttl = Timer(random_time, self.delete_process)
                ttl.start()

    def _set_circuit_info(self):
        """
        Extracts the type, A and Z sides from self.event_text.
        Updates `self.link_type`, `self.side_a` and `self.side_z` accordingly.

        >>> from src.longhorn.process.process_functions import Process
        >>> process = Process('LINK DOWN | TRANSIT-LON<>CAR | A3', _ut=True)
        >>> process._set_circuit_info()
        ['TRANSIT', 'LON', 'CAR']
        """
        identifier = search(
            r"[a-zA-Z]*-[a-zA-Z0-9]*<>[a-zA-Z0-9]*", self.event_text
        ).group()
        site_ends = str(
            search(r"[a-zA-Z0-9]*<>[a-zA-Z0-9]*", identifier).group()
        ).split("<>")
        self.link_type = identifier.split("-")[0]
        self.side_a = site_ends[0]
        self.side_z = site_ends[1]
        return [self.link_type, self.side_a, self.side_z]

    def _get_duplicate_requests(self, process_file: str):
        """
        Checks to see if `self.side_a` and `self.side_z` exists in the CSV file.
        It appends any lines that do not match to a list and returns the results.

        :param process_file: The location where the CSV file is located to track processes
        """
        duplicate_requests = []

        with open(process_file, "rt", encoding="utf-8") as opened_process_file:
            running_processes = reader(opened_process_file)

            for row in running_processes:
                if self.side_a in row and self.side_z in row:
                    duplicate_requests.append(row)

        return duplicate_requests

    def _check_time_is_between(self, start: datetime, end: datetime):
        """
        Returns a boolean value based on if self.hold_start is between the 'start' and 'end' times.

        :param start: The beginning of the timeframe `self.hold_start` is checked for
        :param end: The end of the timeframe `self.hold_start` is checked for
        """
        if start <= end:
            return start <= self.hold_start <= end
        return False

    @staticmethod
    def _convert_date_string_to_datetime(string_datetime: str):
        """
        Converts a datetime in string format into a datetime() object.
        Returns None on incorrect type.

        :param string_datetime: Datetime in string format (e.g. YYYY-MM-DD HH:MM:SS)
        """
        try:
            date = string_datetime.split(" ")[0]
            time = string_datetime.split(" ")[1]
            year = int(date.split("-")[0])
            month = int(date.split("-")[1])
            day = int(date.split("-")[2])
            hour = int(time.split(":")[0])
            minute = int(float(time.split(":")[1]))
            second = int(float(time.split(":")[2]))
            if match(
                r"^[0-9]{4}([-/][0-9]{2}){2} [0-9]{2}(:[0-9]{2}){2}\.[0-9]{6}$",
                string_datetime,
            ):
                millisecond = int(float(time.split(".")[1]))
                return datetime(year, month, day, hour, minute, second, millisecond)
            return datetime(year, month, day, hour, minute, second)
        except AttributeError:
            pass
        except ValueError:
            pass
        app.logger.error(f"Non-compliant date-time: {string_datetime}")
        return None

    def _check_if_duplicate(self, duplicates: list):
        """
        Checks if another process exists that contains both the same link sites and is a similar time.

        :param duplicates: A list containing the CSV values:
        ID, Circuit Type, Side A, Side Z, Time Logged and Hold Expires.
        """
        for duplicate in duplicates:
            start = self._convert_date_string_to_datetime(duplicate[4])
            end = self._convert_date_string_to_datetime(duplicate[5])
            if self._check_time_is_between(start, end):
                return True
        return False

    def create_process(self):
        """
        Adds the current process into the process file in the format of:
        ID, circuit type, side_a, side_z, hold_start, hold_end.
        """
        with open(self.process_file, "at", encoding="utf-8") as process_file:
            entry = writer(process_file)
            entry.writerow(
                [
                    self.process_id,
                    self.link_type,
                    self.side_a,
                    self.side_z,
                    self.hold_start,
                    self.hold_end,
                ]
            )

    def delete_process(self):
        """
        Loops through the existing entries in the process file until it finds the matching ID.
        If the ID is found the file will be rewritten to remove the entry.
        """
        lines = []
        with open(self.process_file, "rt", encoding="utf-8") as process_file:
            running_processes = reader(process_file)
            for entry in running_processes:
                if self.process_id not in entry:
                    lines.append(entry)

        with open(self.process_file, "wt", encoding="utf-8") as process_file:
            running_processes = writer(process_file)
            running_processes.writerows(lines)


def delete_process_entries(clear_file: str):
    """
    Clears all entries from processes file.

    :param clear_file: process file to clear
    """
    lines = []

    with open(clear_file, "rt", encoding="utf-8") as process_file:
        running_processes = reader(process_file)
        for entry in running_processes:
            lines.append(entry)

    with open(clear_file, "wt", encoding="utf-8") as process_file:
        running_processes = writer(process_file)
        running_processes.writerow(lines[0])


def check_sessions(event_text: str, process_file: str):
    """
    Creates a process for the incoming request.

    :param event_text: The event_text provided in the request data
    :param process_file: Path to process file
    """
    current_process = Process(
        event_text,
        process_file,
        hold_delay_in_seconds=app.config["PROCESS_TTL"],
    )
    return current_process
