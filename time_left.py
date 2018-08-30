#!/usr/bin/env python
# time_left.py --time 15:00 --format_time '%H:%M'

import defopt
from datetime import datetime


def main(*, time="15:00", format_time="%H:%M"):
    """Display a friendly greeting.

    :param str time: Number of times to display the greeting
    :param str format_time: Number of times to display the greeting
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

    time_delta = my_time - time_now
    print(time_delta)


if __name__ == '__main__':
    defopt.run(main)
