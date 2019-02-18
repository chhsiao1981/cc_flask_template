# -*- coding: utf-8 -*-


def timestamp_to_datetime(the_timestamp):
    """timestamp (in sec) to datetime

    Args:
        the_timestamp (int): timestamp in sec

    Returns:
        datetime: datetime
    """
    return datetime.utcfromtimestamp(int(the_timestamp))


def datetime_to_timestamp(the_datetime):
    return calendar.timegm(the_datetime.timetuple())


def datetime_to_microtimestamp(the_datetime):
    return int(calendar.timegm(the_datetime.timetuple()) * 1e6 + the_datetime.microsecond)


def get_timestamp():
    """get current timestamp in sec

    Returns:
        int: current timestamp in sec
    """
    return int(time.time())


def get_milli_timestamp():
    """get current timestamp in milli-sec

    Returns:
        int: current timestamp in milli-sec
    """
    return int(time.time() * 1000.0)


def get_micro_timestamp():
    """get current timestamp in micro-sec

    Returns:
        int: current timestamp in micro-sec
    """
    return int(time.time() * 1000000.0)


def get_hr_timestamp():
    """get current hr-timestamp in sec

    Returns:
        int: current hr-timestamp
    """
    the_timestamp = get_timestamp()
    return timestamp_to_hr_timestamp(the_timestamp)


def timestamp_to_hr_timestamp(the_timestamp):
    """timestamp to hr-timestamp

    Args:
        the_timestamp (int): the timestamp in sec

    Returns:
        int: hr-timestamp
    """
    the_block = int(the_timestamp // 3600)
    return the_block * 3600


def timestamp_to_day_timestamp(the_timestamp):
    """timestamp to day-timestamp

    Args:
        the_timestamp (int): the timestamp in sec

    Returns:
        int: day-timestamp
    """
    the_block = the_timestamp // 86400
    return the_block * 86400


def micro_timestamp_to_datetime(the_microtimestamp):
    """microtimestamp to datetime.

    Args:
        the_microtimestamp (int): the microtimestamp

    Returns:
        datetime: datetime
    """
    return timestamp_to_datetime(the_microtimestamp * MICROTIME_TO_TIME)
