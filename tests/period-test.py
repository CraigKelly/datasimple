"""Tests for helpers for time periods."""

from datetime import datetime, timedelta

from nose.tools import eq_  # ok_

from datasimple.period import Period


def eqf_(f1, f2):
    if abs(f1 - f2) > 0.0000001:
        assert False, '{} != {}'.format(f1, f2)


def period_test():
    # Check date to period and prev/next period
    now = datetime.now()
    pnow = Period.from_dt(now)
    eq_(now.year, pnow.year)
    eq_(now.month, pnow.month)

    last = datetime(now.year, now.month, 1) - timedelta(days=1)
    last = datetime(last.year, last.month, 1)
    plast = pnow.prev_period()
    eq_(last.year, plast.year)
    eq_(last.month, plast.month)

    pnow2 = plast.next_period()
    eq_(now.year, pnow2.year)
    eq_(now.month, pnow2.month)

    # Check CPI init and usage
    curr = pnow
    cpi_data = []
    cpi = 100.0
    for _ in range(13):
        cpi_data.append({'Year': curr.year, 'Month': curr.month, 'CPI': cpi})
        cpi *= 0.95
        curr = curr.prev_period()
    winstart = curr.next_period()

    Period.init_cpi(cpi_data)
    eqf_(100.0, pnow.cpi())
    eqf_(100.0, pnow.adj_price(100.0, 'SO'))
    eqf_(1000.0, pnow.adj_price(100.0, 'CE'))

    window = list(winstart.window())
    eq_(12, len(window))
    # If we got our CPI dummy data correct, then translating a dollar amount
    # from the past into today's dollars should increase that amount
    assert window[0].adj_price(100.0, 'SO') > window[-1].adj_price(100.0, 'SO')
    assert window[0].adj_price(100.0, 'CE') > window[-1].adj_price(100.0, 'CE')
