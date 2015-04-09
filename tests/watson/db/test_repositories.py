# -*- coding: utf-8 -*-
from pytest import raises
from tests.watson.db import support


class TestBaseRepository(object):

    def setup(self):
        self.session = support.session

    def test_create(self):
        with raises(Exception):
            support.TestRepository()
        assert support.TestRepository(self.session)

    def test_new_obj(self):
        repo = support.TestRepository(self.session)
        obj = repo.new(value=2)
        assert obj.value == 2

    def test_query_all(self):
        repo = support.TestRepository(self.session)
        assert len(repo.all()) == 6

    def test_get(self):
        repo = support.TestRepository(self.session)
        repo.get(1).value == 1
        with raises(Exception):
            repo.get(10, error_on_not_found=True)

    def test_first(self):
        repo = support.TestRepository(self.session)
        assert repo.first(id=1).value == '1'

    def test_save_delete(self):
        repo = support.TestRepository(self.session)
        obj = repo.new(value='test')
        repo.save(obj)
        assert repo.count() == 7
        repo.delete(obj)
        assert repo.count() == 6
        assert not repo.first(value='test')

    def test_save_delete_all(self):
        repo = support.TestRepository(self.session)
        obj = repo.new(value='test')
        obj2 = repo.new(value='test2')
        repo.save_all(obj, obj2)
        assert repo.first(value='test2')
        repo.delete_all(obj, obj2)
        assert not repo.first(value='test2')

    def test_update(self):
        with raises(NotImplementedError):
            support.TestRepository(self.session).update()
