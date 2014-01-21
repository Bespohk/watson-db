# -*- coding: utf-8 -*-
from tests.watson.db import support


def test_engine_create():
    engine = support.app.container.get('sqlalchemy_engine_default')
    assert engine.execute("select 1").scalar() == 1
