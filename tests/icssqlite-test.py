"""Tests for simple sqlite3 wrapper for ICS data."""

from datasimple.sqlite import connect


def connect_test():
    db = connect(':memory:')
    with db:
        db.execute("""create table t (a, b)""")
        db.execute("""insert into t (a, b) values (' the part is-ok', '06/22/2017')""")

    def v(exp, sql):
        act = list(db.execute(sql))[0][0]
        if exp != act:
            assert exp == act, 'Expected {} but got {}'.format(exp, act)

    v('PARTIS0K', """select comppart(a) from t""")

    v('2017', """select strftime('%Y', ds_datetime(b)) from t""")
    v('06', """select strftime('%m', ds_datetime(b)) from t""")
    v('22', """select strftime('%d', ds_datetime(b)) from t""")

    v('2017', """select strftime('%Y', ds_datetime('08/22/17'))""")
    v('2017', """select strftime('%Y', ds_datetime('08/01/17'))""")
    v('2017', """select strftime('%Y', ds_datetime('8/1/17'))""")
    v('2017', """select strftime('%Y', ds_datetime('08/1/17'))""")
    v('2017', """select strftime('%Y', ds_datetime('8/01/17'))""")
    v('2017', """select strftime('%Y', ds_datetime('08/22/2017'))""")
    v('2017', """select strftime('%Y', ds_datetime('08/01/2017'))""")
    v('2017', """select strftime('%Y', ds_datetime('8/1/2017'))""")
    v('2017', """select strftime('%Y', ds_datetime('08/1/2017'))""")
    v('2017', """select strftime('%Y', ds_datetime('8/01/2017'))""")

    v('08', """select strftime('%m', ds_datetime('08/22/17'))""")
    v('08', """select strftime('%m', ds_datetime('08/01/17'))""")
    v('08', """select strftime('%m', ds_datetime('8/1/17'))""")
    v('08', """select strftime('%m', ds_datetime('08/1/17'))""")
    v('08', """select strftime('%m', ds_datetime('8/01/17'))""")
    v('08', """select strftime('%m', ds_datetime('08/22/2017'))""")
    v('08', """select strftime('%m', ds_datetime('08/01/2017'))""")
    v('08', """select strftime('%m', ds_datetime('8/1/2017'))""")
    v('08', """select strftime('%m', ds_datetime('08/1/2017'))""")
    v('08', """select strftime('%m', ds_datetime('8/01/2017'))""")

    v('22', """select strftime('%d', ds_datetime('08/22/17'))""")
    v('01', """select strftime('%d', ds_datetime('08/01/17'))""")
    v('01', """select strftime('%d', ds_datetime('8/1/17'))""")
    v('01', """select strftime('%d', ds_datetime('08/1/17'))""")
    v('01', """select strftime('%d', ds_datetime('8/01/17'))""")
    v('22', """select strftime('%d', ds_datetime('08/22/2017'))""")
    v('01', """select strftime('%d', ds_datetime('08/01/2017'))""")
    v('01', """select strftime('%d', ds_datetime('8/1/2017'))""")
    v('01', """select strftime('%d', ds_datetime('08/1/2017'))""")
    v('01', """select strftime('%d', ds_datetime('8/01/2017'))""")
