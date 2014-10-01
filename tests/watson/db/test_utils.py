# -*- coding: utf-8 -*-
from pytest import raises
from sqlalchemy.orm import exc
from watson.db import utils
from tests.watson.db.support import session, Test


class TestPaginator(object):

    def test_create_paginator(self):
        paginator = utils.Pagination(session.query(Test))
        assert paginator
        assert repr(paginator) == '<watson.db.utils.Pagination page:1 limit:20 total:6 pages:1>'

    def test_iter_pages(self):
        paginator = utils.Pagination(session.query(Test), page=2, limit=2)
        assert paginator.pages == 3
        assert paginator.has_next
        assert paginator.has_previous
        for page in paginator.iter_pages():
            assert True

    def test_iter_results(self):
        paginator = utils.Pagination(session.query(Test), page=1, limit=2)
        for page in paginator:
            assert True
        if not paginator:
            assert True is False

    def test_no_results(self):
        paginator = utils.Pagination(session.query(Test).filter(Test.value == 10), page=2)
        assert not paginator.has_next
