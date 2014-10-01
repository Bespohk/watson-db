# -*- coding: utf-8 -*-
from pytest import raises
from sqlalchemy import Column, Integer
from sqlalchemy.exc import InvalidRequestError
from watson.db import models


class MyModel(models.Model):
    id = Column(Integer, primary_key=True)


class TestModels(object):
    def test_model(self):
        model = MyModel()
        assert model.__tablename__ == 'my_models'

    def test_invalid_model(self):
        with raises(InvalidRequestError):
            class MyModelNoPrimaryKey(models.Model):
                pass
