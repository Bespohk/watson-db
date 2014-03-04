# -*- coding: utf-8 -*-
from pytest import raises
from watson.db.contextmanagers import transaction_scope
from tests.watson.db.support import session as db, Test


class TestSessionContextManager(object):

    def test_scope(self):
        before = db.query(Test).all()
        with transaction_scope(db) as session:
            obj = Test(value='Test')
            session.add(obj)
        after = db.query(Test).all()
        assert len(before) < len(after)

    def test_scope_exception(self):
        with raises(Exception):
            with transaction_scope(db) as session:
                session.add(Test())

    def test_close_connection(self):
        with transaction_scope(db, should_close=True) as session:
            pass
        assert not session._new
