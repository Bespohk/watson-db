# -*- coding: utf-8 -*-
from watson.db import session
from sqlalchemy.orm.scoping import scoped_session


class TestSession(object):
    def test_create_session(self):
        assert isinstance(session.make_session(), scoped_session)
