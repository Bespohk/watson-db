# -*- coding: utf-8 -*-
from watson.db import panels
from tests.watson.db import support


class TestQueryPanel(object):
    def test_create(self):
        panel = panels.Query({}, support.app.container.get('jinja2_renderer'), support.app)
        assert panel.title == 'Database'

    def test_render(self):
        panel = panels.Query({}, support.app.container.get('jinja2_renderer'), support.app)
        support.app.run(support.sample_environ(), support.start_response)
        assert 'watson-debug-toolbar__panel__debug' in panel.render()
        assert panel.render_key_stat() == '0 queries (0.00ms)'
