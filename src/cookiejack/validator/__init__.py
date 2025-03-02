import argparse
from datetime import datetime


def cookie_date(date_string):
    try:
        datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S GMT")
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date provided; Format should be \"Sun, 01 Jan 2000 00:00:00 GMT\"")

    return date_string
