#!/usr/bin/env python
from random import choice
import sys

WORDS_FILE = '/usr/share/dict/words'


if sys.version_info >= (2, 7):
    def _get_args():
        from argparse import ArgumentParser
        parser = ArgumentParser(description='Get random words.')
        parser.add_argument(
            '-n',
            dest='num_words',
            metavar='num_words',
            type=int,
            default=1,
            help='number of words to return (default = 1)',
        )
        return parser.parse_args()
else:
    def _get_args():
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option(
            '-n',
            dest='num_words',
            metavar='num_words',
            type=int,
            default=1,
            help='number of words to return (default = 1)',
        )
        (options, args) = parser.parse_args()
        return options
    

def get_words(num_words):
    with open(WORDS_FILE) as f:
        words = f.readlines()
    return [choice(words).strip() for _ in range(num_words)]
    

if __name__ == '__main__':
    args = _get_args()
    print(' '.join(get_words(args.num_words)))
