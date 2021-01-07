import math
import pytz
import unittest

from datetime import datetime, timezone, timedelta
from identidoc.services import get_current_time_as_POSIX_timestamp, datetime_to_POSIX_timestamp

class TestMiscFunctions(unittest.TestCase):
    # This test is going to be very hard to "test"
    def test_get_current_time_as_POSIX_timestamp(self):
        current_time = datetime.now(tz=timezone.utc)

        current_time_test = get_current_time_as_POSIX_timestamp()
        current_time_timestamp = int(current_time.timestamp())

        assert isinstance(current_time_test, int)

        # Just assert that the difference is less than 3 seconds
        assert abs(current_time_test - current_time_timestamp) < 3

    
    def test_datetime_to_POSIX_timestamp(self):
        current_time = datetime.now(tz=timezone.utc)

        utc_timestamp = datetime_to_POSIX_timestamp(current_time)

        for tz in pytz.all_timezones:
            different_timezone = current_time.astimezone(pytz.timezone(tz))
            different_timezone_timestamp = datetime_to_POSIX_timestamp(different_timezone)

            assert utc_timestamp == different_timezone_timestamp
