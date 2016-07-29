# -*- coding: utf-8 -*-
from watson.db import panels
from tests.watson.db import support


class TestQueryPanel(object):
    def test_create(self):
        panel = panels.Query({}, support.app.container.get('jinja2_renderer'), support.app)
        assert panel.title == 'Database'

    def test_render(self):
        panel = panels.Query({}, support.app.container.get('jinja2_renderer'), support.app)
        assert 'watson-debug-toolbar__panel__debug' in panel.render()
