from datetime import datetime
from . import ProcessFunctionsTestCase


class ConvertDateStringToDatetimeTestCase(ProcessFunctionsTestCase):
    def test_convert_date_string_to_datetime_returns_datetime_with_milliseconds_on_regex_match(self):
        self.assertEqual(
            self.process._convert_date_string_to_datetime("1970-01-01 00:00:00.123456"),
            datetime(1970, 1, 1, 0, 0, 0, 123456),
        )

    def test_convert_date_string_to_datetime_returns_datetime_without_milliseconds_on_regex_match(self):
        self.assertEqual(
            self.process._convert_date_string_to_datetime("1970-01-01 00:00:00"),
            datetime(1970, 1, 1, 0, 0, 0),
        )

    def test_convert_date_string_to_datetime_returns_none_on_bad_format(self):
        self.assertIsNone(self.process._convert_date_string_to_datetime("bananas"))

    def test_convert_date_string_to_datetime_handles_type_error_on_wrong_type(self):
        result = self.process._convert_date_string_to_datetime(
            datetime(1970, 1, 1, 0, 0, 0, 123456)
        )
        self.assertIsNone(result)
