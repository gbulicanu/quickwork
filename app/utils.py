""" Utils functions module.
"""
from string import Formatter


def __strfdelta_trim_zero_hours(input_str):
    return input_str.replace("0h ", "").replace(" 0m", "")


def strfdelta(
    time_delta,
    fmt='{D:02}d {H:02}h {M:02}m {S:02}s',
    input_type='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The input_type argument allows time_delta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid input_type strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """

    # Convert time_delta to integer seconds.
    if input_type == 'timedelta':
        remainder = int(time_delta.total_seconds())
    elif input_type in ['s', 'seconds']:
        remainder = int(time_delta)
    elif input_type in ['m', 'minutes']:
        remainder = int(time_delta)*60
    elif input_type in ['h', 'hours']:
        remainder = int(time_delta)*3600
    elif input_type in ['d', 'days']:
        remainder = int(time_delta)*86400
    elif input_type in ['w', 'weeks']:
        remainder = int(time_delta)*604800

    formatter = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in formatter.parse(fmt)]
    possible_fields = ('W', 'D', 'H', 'M', 'S')
    constants = {'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])
    return __strfdelta_trim_zero_hours(formatter.format(fmt, **values))
