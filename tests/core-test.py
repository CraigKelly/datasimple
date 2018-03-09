"""Tests for simple or fundamental helpers."""

from datasimple.core import compact, first, first_in, kv, norm_ws


def core_test():
    assert compact([]) == [], 'Empty list'
    assert compact([0, '', set(), dict(), []]) == [], 'Empty list from nothings'
    assert compact([0, 1, 2, 0]) == [1, 2], 'Empty bookends'
    assert compact([1, 0, 0, 2]) == [1, 2], 'Empty internals'
    assert compact(range(3)) == [1, 2], 'Iterator'


def first_test():
    assert first([]) is None, 'Empty iterator'
    assert first([1]) == 1, 'Single item'
    assert first([42, 1]) == 42, 'Multi item'


def first_in_test():
    def assertf(exp, act, msg):
        assert abs(exp-act) < 0.00000001, msg

    assert first_in(defval=1) == 1, 'Empty'
    assertf(42.0, first_in('a', {}, -0.00001, 42, func=float, floor=0.0), 'Doc Example')
    assertf(-12.345, first_in('a', {}, 42, -12.345, func=float, ceil='41'), 'Text Ceiling')

    assert 1 == first_in(*(1, 2, 3), func=lambda x: int(x)-1, floor=1, ceil=3), 'Extra int work'


def kv_test():
    assert ('k', 'v') == kv('k:v'), 'easy default'
    assert ('k', 'v') == kv(' k:v'), 'space checking'
    assert ('k', 'v') == kv('k:v '), 'space checking'
    assert ('k', 'v') == kv(' k : v '), 'space checking'
    assert ('k', 'v:v:v') == kv('k: v:v:v'), 'delim in value'
    assert ('k', '') == kv('k'), 'no value'
    assert ('k', '') == kv('k:'), 'no value'


def norm_ws_test():
    assert '' == norm_ws(''), 'empty string'
    assert 'a b c' == norm_ws(' a b c '), 'simple trim'
    assert 'a b c' == norm_ws(' a \t b \r c \n '), 'multi spacing'
