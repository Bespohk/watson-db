# -*- coding: utf-8 -*-
from watson.db import utils
from tests.watson.db.support import session, Test


class TestPaginator(object):

    def test_create_paginator(self):
        paginator = utils.Pagination(session.query(Test))
        expects = '<watson.db.utils.Pagination page:1 limit:20 total:6 pages:1>'
        assert paginator
        assert repr(paginator) == expects

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

    def test_next_previous_page(self):
        paginator = utils.Pagination(session.query(Test), page=2, limit=2)
        assert paginator.next.id == 3
        assert paginator.previous.id == 1

        paginator = utils.Pagination(session.query(Test), page=1, limit=2)
        assert not paginator.previous
        paginator = utils.Pagination(session.query(Test), page=3, limit=2)
        assert not paginator.next

    def test_page_query_string(self):
        paginator = utils.Pagination(session.query(Test), page=2, limit=2)
        assert str(paginator.next) == '?page=3'
        assert str(paginator.previous) == '?page=1'

    def test_page_query_string_append(self):
        paginator = utils.Pagination(session.query(Test), page=2, limit=2)
        paginator.next.append(test='test')
        next_query = str(paginator.next)
        assert 'test=test' in next_query
        assert 'page=3' in next_query
        paginator.next.append(anothervalue='value')
        next_query = str(paginator.next)
        assert 'anothervalue=value' in next_query
        assert 'test=test' in next_query
        paginator.previous.append(test='test')
        prev_query = str(paginator.previous)
        assert 'page=1' in prev_query

    def test_paginator_query_string_from_dict(self):
        existing_get = {'page': 1, 'test': 'test'}
        paginator = utils.Pagination(session.query(Test), page=2, limit=2)
        paginator.next.append(**existing_get)
        next_query = str(paginator.next)
        assert 'test=test' in next_query
        assert 'page=3' in next_query
