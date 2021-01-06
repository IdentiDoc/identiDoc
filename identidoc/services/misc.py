# This file will include an index of shared routines that are needed in multiple components of identidoc

from datetime import timezone, datetime


def get_current_time_as_POSIX_timestamp():
    return datetime_to_POSIX_timestamp(datetime.now(tz=timezone.utc))


# This function needs to be called to ensure timestamp consistency between
# file upload and query timestamps
def datetime_to_POSIX_timestamp(datetime_to_convert):
    return int(datetime_to_convert.timestamp())