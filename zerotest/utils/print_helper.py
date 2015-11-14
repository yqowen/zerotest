from __future__ import print_function

__author__ = 'Hari Jiang'

_DEFAULT_LINE_NOTIFY_FORMAT = '{:=^120}'


def print_line_notify(msg):
    print(_DEFAULT_LINE_NOTIFY_FORMAT.format(" {} ".format(msg)))
