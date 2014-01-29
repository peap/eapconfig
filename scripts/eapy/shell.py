#!/usr/bin/env python
"""
Utilities for system scripts
"""
import os
import subprocess
import sys

COLOR_GRAY = '30'
COLOR_RED = '31'
COLOR_GREEN = '32'
COLOR_YELLOW = '33'
COLOR_BLUE = '34'
COLOR_MAGENTA = '35'
COLOR_CYAN = '36'
COLOR_WHITE = '37'
COLOR_CRIMSON = '38'


def colorize(msg, color):
    """
    Wrap a message in shell color codes.
    """
    return '\033[1;{0}m{1}\033[1;m'.format(color, msg)


def uncolorize(msg):
    """
    Strip shell color codes from a string
    """
    code = '\033[1;'
    if msg.find(code) >= 0:
        msg = msg.replace(code, '')[3:-1]
    return msg


def ensure_commands_exist(commands, exit_code=1):
    """
    Ensure that all commands given by an iterable exist, otherwise exit.
    """
    commands_exist = map(command_available, commands)
    if not all(commands_exist):
        sys.exit(exit_code)
    return None


def command_available(command, print_error=True):
    """
    See if a command exists by trying to call it with --help.
    """
    devnull = open(os.devnull, 'w')
    try:
        subprocess.call(
            [command, '--help'],
            stdout=devnull,
            stderr=devnull,
        )
        return True
    except OSError as e:
        if print_error:
            print('You must install {0}.'.format(command))
        return False
    finally:
        devnull.close()


class PPTable(object):
    """
    Pretty-print a table.
    """
    def __init__(self, cols, data=None):
        self.cols = cols
        self.data = data or []

    def add_data(self, data):
        self.data.append(data)

    def _col_width(self, col_index):
        if self.data:
            max_data_width = max([len(uncolorize(d[col_index])) for d in self.data])
        else:
            max_data_width = 0
        return max(len(self.cols[col_index]), max_data_width)

    @property
    def header(self):
        h = []
        for i, col in enumerate(self.cols):
            width = self._col_width(i)
            h.append('{0:<{width}}'.format(col, width=width))
        return ' | '.join([''] + h + ['']).strip()

    @property
    def rows(self):
        lines = []
        for row in self.data:
            r = []
            for i, value in enumerate(row):
                width = self._col_width(i)
                if len(value) > width:
                    width = len(value) + (width - len(uncolorize(value)))
                val = '{0:<{width}}'.format(value, width=width)
                r.append(val)
            lines.append(' | '.join([''] + r + ['']).strip())
        return '\n'.join(lines)

    def __str__(self):
        horizontal_border = '+' + '-'*(len(self.header)-2) + '+'
        return '\n'.join([
            horizontal_border,
            self.header,
            horizontal_border,
            self.rows,
            horizontal_border,
        ])
