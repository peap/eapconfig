#!/usr/bin/env python
"""
Utilities for system scripts
"""
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
    try:
        subprocess.call(
            [command, '--help'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except OSError as e:
        if print_error:
            print('You must install {0}.'.format(command))
        return False
