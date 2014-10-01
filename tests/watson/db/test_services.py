# -*- coding: utf-8 -*-
from pytest import raises
from tests.watson.db import support


class TestBaseService(object):

    def setup(self):
        self.session = support.session

    def test_create(self):
        with raises(Exception):
            support.TestService()
        assert support.TestService(self.session)

    def test_new_obj(self):
        service = support.TestService(self.session)
        obj = service.new(value=2)
        assert obj.value == 2

    def test_query_all(self):
        service = support.TestService(self.session)
        assert len(service.all()) == 6

    def test_get(self):
        service = support.TestService(self.session)
        service.get(1).value == 1
        with raises(Exception):
            service.get(10, error_on_not_found=True)

    def test_first(self):
        service = support.TestService(self.session)
        assert service.first(id=1).value == '1'

    def test_save_delete(self):
        service = support.TestService(self.session)
        obj = service.new(value='test')
        service.save(obj)
        assert service.count() == 7
        service.delete(obj)
        assert service.count() == 6
        assert not service.first(value='test')

    def test_save_delete_all(self):
        service = support.TestService(self.session)
        obj = service.new(value='test')
        obj2 = service.new(value='test2')
        service.save_all(obj, obj2)
        assert service.first(value='test2')
        service.delete_all(obj, obj2)
        assert not service.first(value='test2')

    def test_update(self):
        with raises(NotImplementedError):
            support.TestService(self.session).update()
