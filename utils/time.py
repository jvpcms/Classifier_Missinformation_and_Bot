from datetime import datetime
import time


def time_struct_to_datetime(ts: time.struct_time | None) -> datetime | None:
    """Convert time.struct_time to datetime"""
    if ts is None:
        return None

    return datetime.fromtimestamp(time.mktime(ts))
