#!/usr/bin/env python
"""
Maintain a directory at ~/remotefs/ for mounting remote filesystems over SSH.
"""
import argparse
import os
import pickle
import subprocess
import sys

from eapy.shell import (
    ensure_commands_exist, PPTable,
    colorize, COLOR_GREEN, COLOR_RED, COLOR_CYAN, COLOR_YELLOW,
)

PROGRAM = 'remotefs'
VERSION = (1, 2, 0)


def _get_version():
    return '.'.join(map(str, VERSION))


REQUIRED_COMMANDS = ('sshfs', 'fusermount')

ACTION_UP = 'up'
ACTION_DOWN = 'down'
ACTION_STATUS = 'status'
ACTION_FORGET = 'forget'
VALID_ACTIONS = (ACTION_UP, ACTION_DOWN, ACTION_STATUS, ACTION_FORGET)


def _get_args():
    parser = argparse.ArgumentParser(prog=PROGRAM, description=__doc__)
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='{0}, v.{1}'.format(PROGRAM, _get_version()),
    )
    parser.add_argument(
        'action',
        nargs='?',
        default=ACTION_STATUS,
        choices=VALID_ACTIONS,
        help=(
            'Mount (up), unmount (down), display the status of, or forget the '
            'named ssh_host. An ssh_host is required for the up and forget '
            'commands, whereas down and status will operate on all known hosts.'
        ),
    )
    parser.add_argument(
        'ssh_host',
        nargs='?',
        help='the ssh host to connect to',
    )
    parser.add_argument(
        '-d', '--directory',
        help='local directory name to use',
    )
    parser.add_argument(
        '-r', '--remote_path',
        default='/',
        help='remote path to mount',
    )
    return parser.parse_args()


class Host(object):
    HOME_DIR = os.path.expanduser('~')
    MOUNT_BASE = os.path.join(HOME_DIR, PROGRAM)
    PICKLE_FILE = os.path.join(MOUNT_BASE, 'remotefs.p')
    CONNECT_TIMEOUT_SECONDS = 5
    STATUS_UP = colorize('up', COLOR_GREEN)
    STATUS_DOWN = colorize('down', COLOR_RED)
    STATUS_UNKNOWN = colorize('unknown', COLOR_YELLOW)

    def __init__(self, name, remote_path='/', rel_path=None):
        hosts = self._get_state()
        host = hosts.get(name, None)
        if host is None:
            if rel_path is None:
                rel_path = host
            host = {
                'name': name,
                'remote_path': remote_path,
                'local_path': os.path.join(self.MOUNT_BASE, rel_path),
                'status': self.STATUS_UNKNOWN,
            }

        self.name = host['name']
        self.remote_path = host['remote_path']
        self.local_path = host['local_path']
        self.status = host['status']

    def save(self):
        hosts = self._get_state()
        host = {
            'name': self.name,
            'remote_path': self.remote_path,
            'local_path': self.local_path,
            'status': self.status,
        }
        hosts.update({self.name: host})
        self._save_state(hosts)

    def mount(self):
        if self.status == self.STATUS_UP:
            return None
        print('Mounting {0}:{1} at {2}...'.format(
            colorize(self.name, COLOR_GREEN),
            colorize(self.remote_path, COLOR_CYAN),
            colorize(self.local_path, COLOR_YELLOW),
        ), end='')
        if not os.path.exists(self.local_path):
            os.mkdir(self.local_path)
        return_code = subprocess.call([
            'sshfs',
            '{0}:{1}'.format(self.name, self.remote_path),
            self.local_path,
            '-o', 'ConnectTimeout={0}'.format(self.CONNECT_TIMEOUT_SECONDS),
        ])
        if return_code == 0:
            self.status = self.STATUS_UP
            print(colorize('ok', COLOR_GREEN))
        else:
            os.rmdir(self.local_path)
            self.status = self.STATUS_DOWN
            print(colorize('fail', COLOR_RED))
        self.save()

    def unmount(self):
        if self.status == self.STATUS_DOWN:
            return None
        print('Unmounting {0}...'.format(
            colorize(self.local_path, COLOR_YELLOW)), end='')
        return_code = subprocess.call([
            'fusermount',
            '-u',
            self.local_path,
        ])
        if return_code == 0:
            os.rmdir(self.local_path)
            self.status = self.STATUS_DOWN
            print(colorize('ok', COLOR_GREEN))
        self.save()

    def forget(self):
        hosts = self._get_state()
        hosts.pop(self.name, None)
        self._save_state(hosts)

    def print_status_line(self):
        print('{0}: {1}'.format(self.name, self.status))

    @classmethod
    def all(cls):
        host_list = []
        hosts = cls._get_state()
        for host in hosts.keys():
            host_list.append(cls(host))
        return host_list

    @classmethod
    def _get_state(cls):
        try:
            hosts = pickle.load(open(cls.PICKLE_FILE, 'rb'))
        except FileNotFoundError as e:
            hosts = {}
        return hosts

    @classmethod
    def _save_state(cls, hosts):
        pickle.dump(hosts, open(cls.PICKLE_FILE, 'wb'))
        

if __name__ == '__main__':
    ensure_commands_exist(REQUIRED_COMMANDS)

    if not os.path.exists(Host.MOUNT_BASE):
        os.mkdir(Host.MOUNT_BASE)

    args = _get_args()
    action = args.action
    ssh_host = args.ssh_host or None

    if ssh_host:
        remote_path = args.remote_path
        rel_path = args.directory or args.ssh_host
        host = Host(ssh_host, remote_path=remote_path, rel_path=rel_path)

        if action == ACTION_FORGET:
            host.forget()
        elif action == ACTION_STATUS:
            table = PPTable(['host', 'status', 'local_path', 'remote_path'])
            table.add_data([host.name, host.status, host.local_path, host.remote_path])
            print(table)
        elif action == ACTION_UP:
            host.mount()
        elif action == ACTION_DOWN:
            host.unmount()
    else:
        if action == ACTION_STATUS:
            table = PPTable(['host', 'status', 'local_path', 'remote_path'])
            for host in Host.all():
                table.add_data([host.name, host.status, host.local_path, host.remote_path])
            print(table)
        elif action == ACTION_DOWN:
            for host in Host.all():
                host.unmount()
        else:
            print(colorize('You must specify a host.', COLOR_RED))
            sys.exit(5)

    sys.exit(0)
