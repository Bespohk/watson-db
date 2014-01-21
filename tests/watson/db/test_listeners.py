# -*- coding: utf-8 -*-
from pytest import raises
from watson.events import types
from watson.framework import applications, events
from tests.watson.db import support


class TestListeners(object):
    def test_init(self):
        app = support.app
        assert app.config['db']

    def test_no_db_config(self):
        with raises(ValueError):
            applications.Http({
                'events': {
                    events.INIT: [
                        ('watson.db.listeners.Init', 1, True)
                    ],
                }
            })

    def test_complete(self):
        app = support.app
        app.dispatcher.trigger(types.Event('event.mvc.complete', target=app))
