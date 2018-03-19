#!/usr/bin/env python3

"""Read stdin, transform the text, and write to stdout

All text is treated as a Python string format. Variables are passed on the
command line and taken from environment variables. Command line beats
environment.

For example:

    echo "{A:} {B:}" | A=Hello B=World ./template-expand.py B=You

would output "Hello You"
"""

import os
import sys


def parse_args():
    for a in sys.argv[1:]:
        comps = a.split('=')
        if len(comps) > 1:
            yield comps[0], '='.join(comps[1:])


def main():
    template_vars = {
        **dict(os.environ),
        **dict(parse_args())
    }

    if template_vars.get('verbose', False):
        sys.stderr.write('Writing template vars to stderr...\n')
        for k, v in sorted(template_vars.items()):
            sys.stderr.write(' {} ==> "{}"\n'.format(k, v))

    sys.stdout.write(
        sys.stdin.read().format(**template_vars)
    )
    sys.stdout.flush()


if __name__ == '__main__':
    main()
