#!/usr/bin/env python
import argparse
from random import choice

WORDS_FILE = '/usr/share/dict/words'


def _get_args():
    parser = argparse.ArgumentParser(description='Get random words.')
    parser.add_argument(
        '-n',
        dest='num_words',
        metavar='num_words',
        type=int,
        default=1,
        help='number of words to return (default = 1)',
    )
    return parser.parse_args()
    

def get_words(num_words):
    with open(WORDS_FILE) as f:
        words = f.readlines()
    return [choice(words).strip() for _ in range(num_words)]
    

if __name__ == '__main__':
    args = _get_args()
    print(' '.join(get_words(args.num_words)))
