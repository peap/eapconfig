"""
Utilities for system scripts:
* ANSI-colorize output
* Pretty-printed tables
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


def colorize(msg, color):
    """
    Wrap a message in ANSI color codes.
    """
    return '\033[1;{0}m{1}\033[1;m'.format(color, msg)


def uncolorize(msg):
    """
    Strip ANSI color codes from a string.
    """
    code = '\033[1;'
    if msg.find(code) >= 0:
        msg = msg.replace(code, '')[3:-1]
    return msg


def ensure_commands_exist(commands, exit_code=1):
    """
    Ensure that all commands given by an iterable exist, otherwise exit (with
    exit_code that defaults to 1).
    """
    commands_exist = map(command_available, commands)
    if not all(commands_exist):
        sys.exit(exit_code)
    return None


def command_available(command, print_error=True):
    """
    See if a command exists by trying to call it with --help.
    """
    exists = False
    with open(os.devnull, 'w') as devnull:
        try:
            subprocess.call([command, '--help'], stdout=devnull, stderr=devnull)
        except OSError as e:
            if print_error:
                print('You must install {0}.'.format(command))
        else:
            exists = True
    return exists


class PPTable(object):
    """
    A table to be pretty-printed to the command line.
    """
    def __init__(self, cols, rows=None):
        self._cols = cols
        self._rows = rows or []

    def add_row(self, row):
        self._rows.append(row)

    def get_col_width(self, col_index):
        header_width = len(self._cols[col_index])
        if self._rows:
            max_cell_width = max([len(uncolorize(row[col_index])) for row in self._rows])
        else:
            max_cell_width = 0
        return max(header_width, max_cell_width)

    def _format_cell(self, i, data):
        width = self.get_col_width(i)
        if len(data) > width:
            width = len(data) + (width - len(uncolorize(data)))
        return '{0:<{width}}'.format(data, width=width)

    def _format_cells(self, cells):
        return ' | '.join([''] + cells + ['']).strip()
        
    @property
    def header(self):
        cells = [self._format_cell(i, cell) for i, cell in enumerate(self._cols)]
        return self._format_cells(cells)

    @property
    def body(self):
        lines = []
        for row in self._rows:
            cells = [self._format_cell(i, cell) for i, cell in enumerate(row)]
            lines.append(self._format_cells(cells))
        return '\n'.join(lines)

    def __str__(self):
        horizontal_border = '+' + '-'*(len(self.header)-2) + '+'
        return '\n'.join([
            horizontal_border,
            self.header,
            horizontal_border,
            self.body,
            horizontal_border,
        ])
