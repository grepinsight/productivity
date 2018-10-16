#!/usr/bin/env python3
import re
import sys

import time_left
import defopt

from colorama import init
from termcolor import colored


# 2672566512 p1                     #spec_dashboard                             Get salesforce to get clinical outcomes
# 2820335919 p1 18/09/19(Wed) 10:00 #Counsyl                                    Prepare talk for tomorrow
# 2809943670 p1 18/09/20(Thu)       #Counsyl        @talks                      Give a talk at Compbio
# 2795236634 p1 18/09/26(Wed) 19:30 #Social         @GCal                       Reservation at AL's Place
# 2812040692 p1 18/09/26(Wed) 07:00 #Counsyl        @people                     @kdauria last day


TIME_PATTERN_0 = r'\d{2}\/\d{2}\/\d{2}\([A-Z][a-z][a-z]\)'
TIME_PATTERN_1 = r'\d{2}\/\d{2}\/\d{2}\([A-Z][a-z][a-z]\) \d{2}:\d{2}'

TEST_STRING0 = "18/09/30(Sun)"
TEST_STRING1 = "18/09/30(Sun) 20:00"
TEST_STRING2 = ""


def map_time_type(text):

    regex_time0 = re.compile(TIME_PATTERN_0)

    regex_time1 = re.compile(TIME_PATTERN_1)

    m1 = regex_time1.search(text)

    m0 = regex_time0.search(text)

    if m0 and m1:
        time_l = time_left.main(time=m1.group(0), format_time='%y/%m/%d(%a) %H:%M', out_format='{D}d {H}h {M:02}m {S:02}s', stdout=False)
        msg = "{:20} - ".format(time_l.rstrip("\n"))
        print(colored(msg, "green"), end="")
    elif m0:
        time_l = time_left.main(time=m0.group(0), format_time='%y/%m/%d(%a)', out_format='{D}d {H}h {M:02}m {S:02}s', stdout=False)
        msg = "{:20} - ".format(time_l.rstrip("\n"))
        print(colored(msg, "green"), end="")
    else:
        msg = "{:20} - ".format("NA")
        print(colored(msg, "red"), end="")


def main():
    for line in sys.stdin:
        map_time_type(line)
        print(line, end='')

if __name__ == '__main__':
    defopt.run(main)
