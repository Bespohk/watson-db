# -*- coding: utf-8 -*-
import os
import shutil
from watson.console.runner import ConsoleError
from watson.db import commands
from sqlalchemy import engine
from sqlalchemy.orm import session
from pytest import raises
from tests.watson.db import support
from watson.common.contextmanagers import suppress


class TestAlembicConfig(object):
    def test_template_directory(self):
        config = commands.Config()
        assert config.get_template_directory().endswith(
            os.path.join('alembic', 'templates'))


class TestDatabase(object):
    def setup(self):
        self.command = commands.Database({
            'connections': {
                'default': {
                    'metadata': 'tests.watson.db.support.Model',
                    'connection_string': 'sqlite:///:memory:'
                }
            }
        })
        self.command.container = support.app.container

    def test_metadata(self):
        assert self.command.metadata['default']

    def test_connections(self):
        assert self.command.connections['default'] == 'sqlite:///:memory:'

    def test_engines(self):
        assert isinstance(self.command.engines['default'], engine.Engine)

    def test_sessions(self):
        assert isinstance(self.command.sessions['default'], session.Session)

    def test_create_command(self):
        assert self.command.create(drop=False)

    def test_populate_command(self):
        assert not self.command.populate()
        command = commands.Database({
            'connections': {
                'default': {
                    'metadata': 'tests.watson.db.support.Model',
                    'connection_string': 'sqlite:///:memory:',
                }
            },
            'fixtures': {
                'path': 'tests/watson/db/fixtures/',
                'data': (
                    ('dummy', None),
                )
            }
        })
        command.container = support.app.container
        assert command.populate()

    def test_dump(self):
        assert self.command.dump()


class TestMigrate(object):
    def setup(self):
        self.command = commands.Migrate({
            'connections': {
                'default': {
                    'metadata': 'tests.watson.db.support.Model',
                    'connection_string': 'sqlite:///:memory:'
                }
            },
            'migrations': {
                'path': 'tests/watson/db/migrations',
                'use_twophase': False
            }
        })
        self.command.container = support.app.container

    def test_database_names(self):
        assert 'default' in self.command.database_names

    def test_directory(self):
        assert self.command.directory.endswith(
            os.path.join('tests', 'watson', 'db', 'migrations'))

    def test_alembic_config_location(self):
        assert self.command.alembic_config_file.endswith(
            os.path.join('tests', 'watson', 'db', 'migrations', 'alembic.ini'))

    def test_invalid_config(self):
        command = commands.Migrate({})
        with raises(ConsoleError):
            command._check_migrations()

    def test_init(self):
        path = ('tests', 'watson', 'db', 'migrations')
        os_path = os.path.join(*path)
        with suppress(Exception):
            shutil.rmtree(os_path)
        assert self.command.init()
        assert os.path.exists(os_path)

    def test_history(self):
        assert self.command.history('head:head')

    def test_current(self):
        assert self.command.current()

    def test_revision(self):
        rev = self.command.revision()
        assert '(head), empty message' in str(rev)

    def test_stamp(self):
        assert self.command.stamp()

    def test_upgrade(self):
        assert self.command.upgrade()

    def test_downgrade(self):
        assert self.command.downgrade()

    def test_branches(self):
        assert self.command.branches()
