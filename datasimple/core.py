"""Simple or fundamental helpers."""

import re
import sys
import traceback

from .cli import log


_comppart_filt = re.compile(r'[^0-9A-Z]+')


def comppart(s):
    """Compress Part Number (or SKU or serial number or similar string).

    To compress a part number:
        - Upper case the string
        - Remove all non-alphanumeric characters
        - Replace all O's (letter oh) with 0 (zero's)
        - Remove the prefix "THE"
    """
    s = str(s).strip().upper().replace('O', '0')
    s = _comppart_filt.sub('', s)
    if s.startswith('THE'):
        s = s[3:]

    return s


def compact(src):
    """Return a list of only truthy values in src."""
    return [i for i in src if i]


def first(t):
    """Return first item in array or None."""
    return t[0] if t else None


def first_in(*args, func=None, floor=None, ceil=None, defval=None):
    """Return first not-None value in args after applying func.

    Optionally require value is > floor and/or < ceil.

    If specified, floor and/or ceil will be converted with func.

    If nothing is found, then defval will be returned.

    An an example, to get the first positive, valid float you can do this:

        first_in('a', {}, -0.00001, 42, func=float, floor=0.0)

    Which should return 42.0.
    """
    if floor is not None:
        floor = func(floor)
    if ceil is not None:
        ceil = func(ceil)

    for a in args:
        try:
            v = func(a)
        except Exception:
            continue
        if floor is not None and v <= floor:
            continue
        if ceil is not None and v >= ceil:
            continue
        return v
    return defval


def kv(s, delim=':'):
    """Parse a field of the format "key: value"."""
    flds = [i.strip() for i in s.split(delim) if i.strip()]
    if len(flds) < 2:
        return first(flds), ''
    return first(flds), delim.join(flds[1:])


def norm_ws(s):
    """Normalize whitespace in the given string."""
    return ' '.join(s.strip().split())


# Used by xl.ValueMapper and test by xl tests
def read_config(cfg_text):
    """Given the contents of config file, use configparser to return a dict."""
    from configparser import ConfigParser

    # For now, hide this class
    class _MyParser(ConfigParser):
        def as_dict(self):
            d = dict(self._sections)
            for k in d:
                d[k] = dict(self._defaults, **d[k])
                d[k].pop('__name__', None)
            return d
    config = _MyParser()
    config.interpolation = None
    config.optionxform = str
    config.read_string(cfg_text)
    return config.as_dict()


def panic(excep):
    """Given an exception, print some info and do a tradition panic."""
    exc_args = sys.exc_info()
    log('FAILED!')
    log(repr(excep))
    traceback.print_exception(*exc_args)
    sys.exit(1)
