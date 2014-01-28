#!/usr/bin/env python
"""
Maintain a directory at ~/remotefs/ for (un)mounting remote filesystems over SSH.
"""
import argparse
import os
import subprocess
import sys

PROGRAM = 'remotefs'
VERSION = (1, 0, 0)

REQUIRED_COMMANDS = ('sshfs', 'fusermount')

HOME_DIR = os.path.expanduser('~')
MOUNT_BASE = os.path.join(HOME_DIR, PROGRAM)

ACTION_UP = 'up'
ACTION_DOWN = 'down'
ACTION_STATUS = 'status'
VALID_ACTIONS = (ACTION_UP, ACTION_DOWN, ACTION_STATUS)

COLOR_GRAY = '30'
COLOR_RED = '31'
COLOR_GREEN = '32'
COLOR_YELLOW = '33'
COLOR_BLUE = '34'
COLOR_MAGENTA = '35'
COLOR_CYAN = '36'
COLOR_WHITE = '37'
COLOR_CRIMSON = '38'

def ensure_commands_exist(commands, exit_code=1):
    commands_exist = map(command_available, commands)
    if not all(commands_exist):
        sys.exit(exit_code)
    return None


def command_available(command, print_error=True):
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


def colorize(msg, color):
    return '\033[1;{0}m{1}\033[1;m'.format(color, msg)

def _get_version():
    return '.'.join(map(str, VERSION))


def _get_args():
    parser = argparse.ArgumentParser(prog=PROGRAM, description=__doc__)
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='{0}, v.{1}'.format(PROGRAM, _get_version()),
    )
    parser.add_argument(
        'action',
        choices=VALID_ACTIONS,
        help='bring the host up or down',
    )
    parser.add_argument(
        'ssh_host',
        nargs='?',
        help='the ssh host to connect to',
    )
    parser.add_argument(
        '-d', '--directory',
        help='directory name to use',
    )
    parser.add_argument(
        '-r', '--remote_path',
        default='/',
        help='remote path to mount',
    )
    return parser.parse_args()


def mount_remote_fs(host, remote_path, local_path):
    if not os.path.exists(MOUNT_BASE):
        os.mkdir(MOUNT_BASE)
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    subprocess.call([
        'sshfs',
        '{0}:{1}'.format(host, remote_path),
        local_path,
    ])
    return None


def unmount_remote_fs(local_path):
    subprocess.call([
        'fusermount',
        '-u',
        local_path,
    ])
    os.rmdir(local_path)
    return None


def status_remote_fs():
    for item in os.listdir(MOUNT_BASE):
        status = colorize('up', COLOR_GREEN)
        print('{0}: {1}'.format(item, status))

if __name__ == '__main__':
    ensure_commands_exist(REQUIRED_COMMANDS)
    args = _get_args()

    if args.action == ACTION_STATUS:
        status_remote_fs()

    if args.action in (ACTION_UP, ACTION_DOWN):
        mount_dir = args.directory or args.ssh_host
        local_path = os.path.join(MOUNT_BASE, mount_dir)

    if args.action == ACTION_UP:
        print('Mounting {0}:{1} at {2}...'.format(
            colorize(args.ssh_host, COLOR_GREEN),
            colorize(args.remote_path, COLOR_CYAN),
            colorize(local_path, COLOR_YELLOW),
        ))
        mount_remote_fs(args.ssh_host, args.remote_path, local_path)
    if args.action == ACTION_DOWN:
        print('Unmounting {0}...'.format(colorize(local_path, COLOR_YELLOW)))
        unmount_remote_fs(local_path)

    sys.exit(0)
