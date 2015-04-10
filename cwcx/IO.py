# coding=utf-8
"""
Input/Output stuff.
"""
import os
import sys
from datetime import datetime

def get_log_filename(filepath):
    """
    Generates a log file path from a given file path.
    :param filepath:
    :return:
    """
    (log_dirname, log_filename) = os.path.split(filepath)
    log_filename = "{date}-{filename}.log".format(date=datetime.now().strftime("%Y-%m-%d"), filename=log_filename)
    log_filename = os.path.join(log_dirname, log_filename)
    return log_filename


def prints(*args, sep=' ', end='\n', file=None):
    """
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

    Prints the values to a stream, or to sys.stdout by default.

    Attaches a local timestamp to the start of the output.

    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    """
    timestamp = "<{0}>".format(datetime.now())
    print(timestamp, *args, sep=sep, end=end, file=file)


class RedirectStdoutTo:

    """
    For redirecting stdout to a file.
    Copied from Dive Into Python.

    Use like:

    with open('log.txt', mode="w", encoding="utf-8") as log_file, RedirectStdoutTo(log_file):
        # do stuff here

    :param out_new:
    """

    def __init__(self, out_new):
        self.out_new = out_new

    def __enter__(self):
        self.out_old = sys.stdout
        sys.stdout = self.out_new

    def __exit__(self, *args):
        sys.stdout = self.out_old
