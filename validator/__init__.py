import argparse
from datetime import datetime


def cookie_date(date_string):
    try:
        datetime.strptime(date_string, "D, d M Y H:i:s \G\M\T")
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date provided")
