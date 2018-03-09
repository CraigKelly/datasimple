#!/usr/bin/env python

"""Given a file name, randomly sample lines and output them to stdout.

You can optionally specify head and tail counts to output before/after sampling
begins.
"""

import argparse
import os.path as path
import random
import sys
import traceback


if sys.version_info[0] < 3:
    raise ValueError('Python 3, please')


def log(msg, *args):
    if args:
        msg = msg.format(*args)
    sys.stderr.write(msg + '\n')
    sys.stderr.flush()


def _err(msg, *args):
    if args:
        msg = msg.format(*args)
    raise ValueError(msg)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-?', '--help', action='help', help='show this help message and exit')
    parser.add_argument('-i', '--input', help='text file to read', required=True)
    parser.add_argument('-h', '--head', help='number of starting lines to output', type=int, default=0)
    parser.add_argument('-t', '--tail', help='number of ending lines to output', type=int, default=0)
    parser.add_argument('-s', '--sample', help='sample rate for lines to output (0.0-1.0)', type=float, default=0.10)
    args = parser.parse_args()

    if not path.isfile(args.input):
        _err('{} does not exist', args.input)
    if args.head < 0:
        _err('head={} but must be >= 0', args.head)
    if args.tail < 0:
        _err('tail={} but must be >= 0', args.tail)
    if args.sample <= 0.0 or args.sample >= 1.0:
        _err('sample={} but must be 0.0-1.0 (exclusive)', args.rate)

    if args.tail > 0:
        log('Pre-reading {}', args.input)
        line_count = 0
        with open(args.input) as inp:
            for _ in inp:
                line_count += 1
        tail_thresh = line_count - args.tail
        log('Done: found {:,d}', line_count)
    else:
        tail_thresh = -1

    curr = 0
    with open(args.input) as inp:
        for line in inp:
            output = False
            curr += 1  # 1-based counting for users

            if curr < args.head:
                output = True
            elif tail_thresh > 0 and curr > tail_thresh:
                output = True
            elif random.random() < args.sample:
                output = True

            if output:
                sys.stdout.write(line)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        exc_args = sys.exc_info()
        log('FAILED! {}\n'.format(e))
        traceback.print_exception(*exc_args, file=sys.stderr)
        sys.exit(1)
