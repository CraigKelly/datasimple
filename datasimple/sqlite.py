"""Simple sqlite3 wrapper.

This is meant to be imported as: `import datasimple.sqlite as sqlite3`

Important: we're only implementing things as we need them.
"""

import sqlite3
import sys

from datetime import datetime

from .core import norm_ws, comppart


def _db_comppart(p):
    # Swallow exceptions for a sqlite function
    try:
        return comppart(p)
    except Exception as e:
        sys.stderr.write('Error with user function:' + repr(e) + '\n')


def _db_customdate_parse(s):
    # manually parse strange date formats
    s = norm_ws(s).split(' ')[0]  # Only up to first space (no time)
    flds = s.split('/')
    if len(flds) == 3:
        mth, day, yr = flds  # m/d/y
    elif len(flds) == 2:
        mth, yr = flds  # m/y
        day = 1
    else:
        return None

    # We go ahead and fail if we can't get our components into int's
    mth, day, yr = (int(f.lstrip('0')) for f in [mth, day, yr])

    # y2k
    if yr < 100:
        yr += 2000

    # Finally done
    return datetime(yr, mth, day)


def _db_datetime(s):
    try:
        if not s:
            return None
        s = str(s).strip()
        if not s:
            return None
        try:
            return _db_customdate_parse(s).strftime('%Y-%m-%d')
        except ValueError as ve:
            return s  # Malformed string - just return the string
    except Exception as e:
        # Handle missed issues - no exceptions returned to sqlite
        sys.stderr.write('Error with user function:' + repr(e) + '\n')


def connect(path):
    """Replace connect that injects our comppart function."""
    conn = sqlite3.connect(path)
    conn.create_function('comppart', 1, _db_comppart)
    conn.create_function('ds_datetime', 1, _db_datetime)
    return conn


def main():
    """Entry point in command line mode."""
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: sqlite.py db SQL', file=sys.stderr)
        return

    db, sql = args

    print('Opening {}'.format(args[0]))
    conn = connect(db)

    for q in sql.split(';'):
        print('Executing {}'.format(q))
        with conn:
            conn.execute(q)


if __name__ == '__main__':
    main()
