# -*- coding: utf-8 -*-
from watson.db import fixtures
from tests.watson.db import support


def test_populate():
    sessions = {'default': support.app.container.get('sqlalchemy_session_default')}

    assert fixtures.populate_all(sessions, {
        'path': 'tests/watson/db/fixtures/',
        'data': (
            ('dummy', None),
        )
    })


def test_populate_to_session():
    fixtures.populate(support.session, 'tests/watson/db/fixtures/dummy.json')
    repo = support.TestRepository(support.session)
    fixture = repo.first(value='Fixture')
    assert fixture
    repo.delete(fixture)
