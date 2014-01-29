#!/usr/bin/env python
"""
Maintain a directory at ~/remotefs/ for (un)mounting remote filesystems over SSH.
"""
import argparse
import os
import pickle
import subprocess
import sys

from eapy.shell import (
    ensure_commands_exist,
    colorize, COLOR_GREEN, COLOR_RED, COLOR_CYAN, COLOR_YELLOW,
)

PROGRAM = 'remotefs'
VERSION = (1, 1, 0)

REQUIRED_COMMANDS = ('sshfs', 'fusermount')
CONNECT_TIMEOUT_SECONDS = 5

HOME_DIR = os.path.expanduser('~')
MOUNT_BASE = os.path.join(HOME_DIR, PROGRAM)
PICKLE_FILE = os.path.join(MOUNT_BASE, 'remotefs.p')

ACTION_UP = 'up'
ACTION_DOWN = 'down'
ACTION_STATUS = 'status'
ACTION_FORGET = 'forget'
VALID_ACTIONS = (ACTION_UP, ACTION_DOWN, ACTION_STATUS, ACTION_FORGET)

STATUS_UP = colorize('up', COLOR_GREEN)
STATUS_DOWN = colorize('down', COLOR_RED)
STATUS_MSG = {
    ACTION_UP: STATUS_UP,
    ACTION_DOWN: STATUS_DOWN,
}


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
        '-o',
        'ConnectTimeout={0}'.format(CONNECT_TIMEOUT_SECONDS),
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


def get_hosts():
    try:
        hosts = pickle.load(open(PICKLE_FILE, 'rb'))
    except FileNotFoundError as e:
        hosts = {}
    return hosts


def save_hosts(hosts):
    pickle.dump(hosts, open(PICKLE_FILE, 'wb'))
    return None
    

def update_host(host, local_path, remote_path, status):
    hosts = get_hosts()
    if host in hosts:
        if hosts[host]['status'] == status:
            raise SystemError('{0} is already {1}'.format(host, status))
    hosts.update({
        host: {
            'local_path': local_path,
            'remote_path': remote_path,
            'status': status,
        }
    })
    save_hosts(hosts)


def forget_host(host):
    hosts = get_hosts()
    hosts.pop(host)
    save_hosts(hosts)


def status_remote_fs():
    hosts = get_hosts()
    for host, props in hosts.items():
        status = STATUS_MSG[props['status']]
        print('{0}: {1}'.format(host, status))


if __name__ == '__main__':
    ensure_commands_exist(REQUIRED_COMMANDS)
    args = _get_args()

    if args.action == ACTION_STATUS:
        status_remote_fs()
        sys.exit(0)

    if args.action == ACTION_FORGET:
        forget_host(args.ssh_host)
        sys.exit(0)

    mount_dir = args.directory or args.ssh_host
    local_path = os.path.join(MOUNT_BASE, mount_dir)
    try:
        update_host(args.ssh_host, local_path, args.remote_path, args.action)
    except SystemError as e:
        print(e)
        sys.exit(1)

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
