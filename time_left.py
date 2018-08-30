#!/usr/bin/env python
# time_left.py --time 15:00 --format_time '%H:%M' --out_format '%M'

from string import Formatter
from datetime import datetime

import defopt


def strfdelta(tdelta,
              fmt='{D:02}d {H:02}h {M:02}m {S:02}s', inputtype='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the strftime() method does for
    datetime.datetime objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid inputtype strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """
    # from https://stackoverflow.com/a/42320260

    # Convert tdelta to integer seconds.
    if inputtype == 'timedelta':
        remainder = int(tdelta.total_seconds())
    elif inputtype in ['s', 'seconds']:
        remainder = int(tdelta)
    elif inputtype in ['m', 'minutes']:
        remainder = int(tdelta)*60
    elif inputtype in ['h', 'hours']:
        remainder = int(tdelta)*3600
    elif inputtype in ['d', 'days']:
        remainder = int(tdelta)*86400
    elif inputtype in ['w', 'weeks']:
        remainder = int(tdelta)*604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ('W', 'D', 'H', 'M', 'S')
    constants = {'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])
    return f.format(fmt, **values)


def main(*,
         time="15:00",
         format_time="%H:%M",
         out_format='{D:02}d {H:02}h {M:02}m {S:02}s'):
    """Display a friendly greeting.

    :param str time: Number of times to display the greeting
    :param str format_time: Number of times to display the greeting
    :param str out_format: output format
    """

    time_now = datetime.now()

    def format_time_builder(time, format_time, missing_format, ref_data):
        if missing_format not in format_time:
            format_time = format_time + '|' + missing_format
            time = time + '|' + str(ref_data)
        return time, format_time

    time, format_time = format_time_builder(time,
                                            format_time, '%Y', time_now.year)
    time, format_time = format_time_builder(time,
                                            format_time, '%m', time_now.month)
    time, format_time = format_time_builder(time,
                                            format_time, '%d', time_now.day)

    my_time = datetime.strptime(time, format_time)

    if(my_time > time_now):
        time_delta = strfdelta(my_time - time_now, out_format)
        print('{}'.format(time_delta))
    else:
        time_delta = strfdelta(time_now - my_time, out_format)
        print('{}'.format(time_delta))


if __name__ == '__main__':
    defopt.run(main)
