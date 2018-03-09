#!/usr/bin/env python

import argparse
import os.path as path
import re
import sys
import csv

from datasimple.cli import log
from datasimple.core import panic


if sys.version_info[0] < 3:
    raise ValueError('Python 3, please')


def _err(msg, *args):
    if args:
        msg = msg.format(*args)
    raise ValueError(msg)


class ReportProcessor(object):
    """Process RPT files."""

    def __init__(self, hdrs, delims, writer):
        self.writer = writer
        self.count = 0
        self.rejects = [
            re.compile(r'^\([0-9,]+ row\(s\) affected\)$'),
        ]

        delim_flds = delims.split()
        assert len(delim_flds) > 1, 'Could not parse delimiters'

        start = 0
        self.space_map = list()

        for s in delim_flds:
            assert len(s.strip('-')) == 0, 'Invalid delimiter spec found'

            ln = len(s)
            assert ln > 0, 'Empty field makes no sense'
            assert len(s) == ln, 'Field creation bug'

            self.space_map.append((start, ln))
            start += (ln + 1)

        if start != len(delims):
            _err('Expected final pos to be {} but was {}', len(delims), start)

        if not self._write_line(hdrs):
            _err('Column name output failed')

    def _write_line(self, line):
        chk = str(line).strip()
        if not chk:
            log('[!r]Skipping blank line[!/r]')
            return False
        for r in self.rejects:
            m = r.match(chk)
            if m:
                log('[!r]Skipping line[!/r]: found [!y]{}[!/y]', m.group(0))
                return False

        self.writer.writerow([
            line[st:st+ln].strip() for st, ln in self.space_map
        ])
        return True

    def process(self, line):
        """Parse and write out the given line."""
        if not self._write_line(line):
            return

        self.count += 1
        if self.count % 100000 == 0:
            log('            Working: wrote [!g]{:,d}[!/g]', self.count)

    def done(self):
        """Do any final processing."""
        log('Processing complete: wrote [!g]{:,d}[!/g]', self.count)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='RPT file to read', required=True)
    parser.add_argument('-o', '--output', help='CSV file to write', required=True)
    parser.add_argument('-e', '--encoding', help='Encoding to read (default utf-8-sig)', default='utf-8-sig')
    args = parser.parse_args()

    if not path.isfile(args.input):
        _err('{} does not exist', args.input)

    log('Opening [!c]{}[!/c]', args.input)
    with open(args.input, encoding='utf-8-sig') as inp:
        hdrs = next(inp)
        delims = next(inp)
        assert hdrs.strip(), 'Missing headers'
        assert delims.strip(), 'Missing delimiters'

        log('Creating [!c]{}[!/c]', args.output)
        with open(args.output, 'w') as outp:
            processor = ReportProcessor(hdrs, delims, csv.writer(outp, quoting=csv.QUOTE_ALL))
            for line in inp:
                processor.process(line)
            processor.done()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        panic(e)
