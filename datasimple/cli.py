"""Helpers for CLI scripts.

IMPORTANT: This is actually our 'prime' module. Many of our modules in this
library expect to be able to import at least cli.log. This has 2 implications:

    1. Failures here will pretty much disable our entire lib
    2. This module should NOT import from any other module in this library

You have been warned.
"""

import os
import re
import sys

import colorclass
if os.name == 'nt':
    colorclass.Windows.enable(auto_colors=True)
else:
    colorclass.set_dark_background()

import terminaltables
Table = terminaltables.AsciiTable


def clr(s, *args, **kwrds):
    """Return a color string, optionally formatted."""
    if args:
        s = s.format(*args, **kwrds)
    color = kwrds.get('color', 'autogreen')
    return colorclass.Color('{%s}%s{/%s}' % (color, s, color))


CLR_ABBREVS = {
    'k': 'autoblack',
    'r': 'autored',
    'g': 'autogreen',
    'y': 'autoyellow',
    'b': 'autoblue',
    'm': 'automagenta',
    'c': 'autocyan',
    'w': 'autowhite',
    'bk': 'autobgblack',
    'br': 'autobgred',
    'bg': 'autobggreen',
    'by': 'autobgyellow',
    'bb': 'autobgblue',
    'bm': 'autobgmagenta',
    'bc': 'autobgcyan',
    'bw': 'autobgwhite',
}
# Include ending tags in lookup
CLR_ABBREVS.update([('/'+k, '/'+v) for k, v in CLR_ABBREVS.items()])


def _matchclr(match):
    """Handle match replacement for clrfmt below.

    We only know how to handle matches with three groups: the opening
    bracket, the color, and the closing bracket.
    """
    assert match
    try:
        pre, val, post = match.group(1, 2, 3)
        if not pre or not post:
            raise ValueError('Malformed clrfmt string')
        parts = [
            pre.replace('[!', '{'),
            CLR_ABBREVS.get(val, val),
            post.replace(']', '}')
        ]
        return ''.join(parts)
    except IndexError:
        return match.group(0)


def clrfmt(s, *args, **kwrds):
    """Our own color bracketting that is compatible with str.format.

    e.g. [!g]Hello World[!/g] becomes {autogreen}Hello World{/autogreen}
    """
    if args or kwrds:
        s = s.format(*args, **kwrds)
    # Note the 3 groups
    s = re.sub(r'(\[!)(/?[A-Za-z]+)(\])', _matchclr, s)
    return colorclass.Color(s)


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARN').upper().strip()
ALLOWED_LEVELS = ('NONE', 'INFO', 'WARN')
if LOG_LEVEL not in ALLOWED_LEVELS:
    raise ValueError('Only supported log levels are: ' + ','.join(ALLOWED_LEVELS))

# pylama:ignore=E302

def _log_is_warn():
    return LOG_LEVEL == 'WARN'

def _log_is_none():
    return LOG_LEVEL == 'NONE'


COLOR_DEFAULT = os.environ.get('COLOR_DEFAULT', 'YES').upper()
if COLOR_DEFAULT:
    COLOR_DEFAULT = COLOR_DEFAULT[0] in 'TY1'  # Accept True or Yes or 1
else:
    COLOR_DEFAULT = False


def warn(msg, *args, **kwrds):
    """Log a warning message.

    Outputs to stderr IFF the log level is WARN.

    The message is formatted and colored red with clr, then written via the
    log function.
    """
    if _log_is_warn():
        log(clr(msg, *args, color='autored', **kwrds))


def default_prefix_text():
    """Return the default static text for log prefixing"""
    import __main__

    return '>'.join([
        os.environ.get('DMK_STEPNAME', ''),
        os.path.split(getattr(__main__, '__file__', ''))[-1]
    ]).strip('>')


_def_text = default_prefix_text()


def log_prefix():
    """Function to generate the prefix for every line written by log.

    By default just returns the DMK_STEPNAME env variable and the file name of
    the currently executing process entry point. Feel free to replace this
    function. :)
    """
    p = _def_text
    global COLOR_DEFAULT
    if COLOR_DEFAULT:
        p = '[!b]' + p + '[!/b]'
    p += ': '

    return p


def use_dynamic_log_prefix(xtra_hdr=None):
    """Replace static log prefix with a dynamic prefix.

    IMPORTANT: Will use color output regardless of COLOR_DEFAULT settings.

    Includes the static log prefix, and a sortable date/time entry. xtra_hdr may
    be a callable or just a string and is added to the header. Color strings are
    allowed (and encouraged)."""

    old = _def_text

    from datetime import datetime

    def _new_log_prefix():
        xtra = xtra_hdr
        while callable(xtra):
            xtra = xtra()
        xtra = ' ' + xtra if xtra else ''

        return '[!b]{old:s}[!/b] [!y]{ts:%Y-%m-%d %H:%M:%S}[!/y]{xtra:} > '.format(**dict(
            old=old,
            ts=datetime.now(),
            xtra=xtra
        ))

    global log_prefix
    log_prefix = _new_log_prefix


def log(msg, *args, docolor=None, **kwrds):
    """Log the given message.

    Outputs to stderr IFF the log level is NOT NONE.

    If docolor is None (the default), it is set from the environment
    variable COLOR_DEFAULT. If True then the msg is formatted with clrfmt.
    If False then msg.format(*args) is used.
    """
    if _log_is_none():
        return  # no logging

    if docolor is None:
        docolor = COLOR_DEFAULT

    prefix = log_prefix()
    if prefix:
        msg = prefix + msg

    if docolor:
        msg = clrfmt(msg, *args, **kwrds)
    elif args or kwrds:
        msg = msg.format(*args, **kwrds)

    sys.stderr.write(msg + '\n')
    sys.stderr.flush()


def log_table(table_name, table_rows, inplace_color=False, justify_columns=None):
    """Using the logging system and terminaltables to output a formatted table.

    If inplace_color then do color formatting on any string-valued cells. Changes
    are made in-place SO BE SURE."""
    log('[!bc][!k]TABLE: {}[!/k][!/bc]', table_name)
    if inplace_color:
        for row in table_rows:
            for idx, cell in enumerate(row):
                if type(cell) is str:
                    row[idx] = clrfmt(cell)
    table = Table(table_rows)
    if justify_columns:
        table.justify_columns.update(justify_columns)
    sys.stderr.write(table.table)
    sys.stderr.write('\n')
    sys.stderr.flush()


# OK, look - it's important to know what your log level is, but this is polluting
# all of our tools. Since the overwhelming majority just use the default (WARN),
# we are only going to explicitly log levels that aren't the default
if LOG_LEVEL != 'WARN':
    log('Log level is {}', clr(LOG_LEVEL, color='autocyan'))


if __name__ == '__main__':
    def _test():
        log(clrfmt('[!r]WARNING[!/r] This is [!c]JUST A VISUAL TEST[!/c]. Not an automated unit test.'))
        global LOG_LEVEL
        LOG_LEVEL = 'NONE'
        log('If you see this it IS AN ERROR')
        warn('If you see this it IS AN ERROR')
        LOG_LEVEL = 'INFO'
        log('Log level info - you should see this')
        warn('If you see this it IS AN ERROR')
        LOG_LEVEL = 'WARN'
        log('Log level info - you should see this')
        warn('Log level warn - you should see this')
        log(clrfmt(
            'clrfmt test: [!g]Green number {:20,d}[!/g] [!br][!w]White-on-Red string {:s}[!/w][!/br]',
            10000000000,
            'FooBar'
        ))
        log(
            'Named fmt test: [!g]{a:s} {b:s} {c:s}[!/g] [!c]{d:s} {e:s}[!/c]',
            a='one', b='2', c='tres', **{'d': 'dict1', 'e': 'dict2'}
        )
        log(
            'Named fmt test dict only: [!g]{a:s} {b:s} {c:s}[!/g] [!c]{d:s} {e:s}[!/c]',
            **{'a': 'one', 'b': '2', 'c': 'tres', 'd': 'dict1', 'e': 'dict2'}
        )
        log_table('Test Table', [
            ['Header 1', 'Header 2'],
            ['Vanilla r1c1', 'Vanilla r1c2'],
            ['Vanilla r2c1', 'Vanilla r2c2'],
            ['Vanilla r3c1', 'Vanilla r3c2'],
        ])
        log_table('Test Table', [
            ['[!br][!w]Header 1[!/w][!/br]', '[!br][!w]Header 2[!/w][!/br]'],
            ['[!c]Blueberry[!/c] r1c1', 'Vanilla r1c2'],
            ['[!c]Blueberry[!/c] r2c1', 'Vanilla r2c2'],
            ['[!c]Blueberry[!/c] r3c1', 'Vanilla r3c2'],
        ], inplace_color=True)

        # Combine previous log prefix with our own
        def x():
            import random
            return '[!br][!w]RND={:.4f}[!/w][!/br]'.format(random.random())

        use_dynamic_log_prefix(x)
        log('[!c]{}[!/c] Look at the dynamic prefix!', '<==')
    _test()
