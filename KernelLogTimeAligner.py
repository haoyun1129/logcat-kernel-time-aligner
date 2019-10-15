#!/usr/bin/env python3
from __future__ import print_function
from contextlib import closing
import fileinput
import sys
import argparse
from datetime import datetime
from enum import Enum

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more version is required.")

SWITCH_PREFIX = '---------'
TIMESTAMP_FORMAT = '%m-%d %H:%M:%S.%f'


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class KernelLogTimeAligner:
    class Buffer(Enum):
        KERNEL = "kernel"
        MAIN = "main"
        RADIO = "radio"
        SYSTEM = "system"

    class State(Enum):
        NORMAL = "normal"
        KERNEL = "kernel"
        KERNEL_LEAVED = "kernel_leaved"

    TAG_KERNEL = "kernel"

    def __init__(self):
        self.state = self.State.NORMAL
        self.ENCODING = "UTF-8"
        self.buffer = None
        self.last_time = None
        self.timestr_length = None

    def analyze(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('file', metavar='FILE', help='files to read, if empty, stdin is used', default=sys.stdin)
        args = parser.parse_args()

        with closing(fileinput.input(args.file, openhook=fileinput.hook_encoded(self.ENCODING))) as finput:
            for line in finput:
                line = line.strip()
                try:
                    self.timestr_length = self.determine_time_string_length(line)
                    break
                except ValueError as e:
                    eprint(e)
                    pass


        with closing(fileinput.input(args.file, openhook=fileinput.hook_encoded(self.ENCODING))) as finput:
            for line in finput:
                line = line.strip()
                if line.startswith(SWITCH_PREFIX):
                    if self.buffer != self.get_buffer(line):
                        self.buffer = self.get_buffer(line)
                        # print("switch to buffer", self.buffer, line)
                elif self.buffer == "kernel" or self.is_kernel_log(line):
                    if self.last_time is not None:
                        pass
                        line = self.replace_time(line, self.last_time)
                else:
                    if line != '\x1a':  # ^Z
                        try:
                            self.last_time = self.parse_time(line)
                        except ValueError as e:
                            eprint(e)
                print(line)

    def parse_time(self, time_string):
        time_string = time_string[:self.timestr_length]  # len("01-09 12:23:36.123") = 18
        dt_obj = datetime.strptime(time_string, TIMESTAMP_FORMAT)
        return dt_obj.timestamp()

    @staticmethod
    def to_time_string(timestamp):
        dt_obj = datetime.fromtimestamp(timestamp)
        return dt_obj.strftime(TIMESTAMP_FORMAT)

    @staticmethod
    def get_buffer(line):
        line = line.strip()
        if line.startswith(SWITCH_PREFIX):
            return line.split()[-1]

    def replace_time(self, line, timestamp):
        line = KernelLogTimeAligner.to_time_string(timestamp)[:self.timestr_length] + line[self.timestr_length:]
        return line

    @staticmethod
    def determine_time_string_length(line):
        """
        Get the length of the time string
        :param line:
        :return: 21 (microsecond) or 18 (millisecond)
        """
        time_string = line[:21]  # len("01-09 12:23:36.123456") = 21
        try:
            dt_obj = datetime.strptime(time_string, TIMESTAMP_FORMAT)
            return 21
        except ValueError:
            time_string = line[:18]
            dt_obj = datetime.strptime(time_string, TIMESTAMP_FORMAT)
            return 18

    @staticmethod
    def is_kernel_log(line):
        splits = line.split()
        if len(splits) < 4:
            return False
        if splits[2] == '0' and splits[3] == '0':
            return True
        else:
            return False


if __name__ == '__main__':
    ja = KernelLogTimeAligner()
    ja.analyze()
