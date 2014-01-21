# -*- coding: utf-8 -*-
from watson.db import session


class TestSession(object):
    def test_create_session(self):
        assert session.Session
