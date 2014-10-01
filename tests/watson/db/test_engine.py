# -*- coding: utf-8 -*-
from tests.watson.db import support
from watson.db.engine import create_db


def test_engine_create():
    engine = support.app.container.get('sqlalchemy_engine_default')
    assert engine.execute("select 1").scalar() == 1


def test_engine_create_db():
    engine = support.app.container.get('sqlalchemy_engine_default')
    create_db(engine, support.Model, drop=True)
    assert engine.execute("select 1").scalar() == 1
