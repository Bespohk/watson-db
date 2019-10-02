# -*- coding: utf-8 -*-
from wsgiref import util
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from watson.framework import applications, events
from watson.db.models import _DeclarativeMeta
from watson.db.repositories import Base


def start_response(status_line, headers):
    pass


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


# Initialize a sample application
app = applications.Http({
    'db': {
        'connections': {
            'default': {
                'connection_string': 'sqlite:///:memory:'
            }
        },
        'fixtures': {
            'path': 'tests/watson/db/fixtures/',
            'data': (
                ('dummy', None),
            )
        }
    },
    'dependencies': {
        'definitions': {}
    },
    'events': {
        events.INIT: [
            ('watson.db.listeners.Init', 1, True)
        ],
    },
    'routes': {
        '/': {
            'path': '/'
        }
    }
})


Model = declarative_base(name='Model', metaclass=_DeclarativeMeta)


class Obj(Model):
    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False)

    def __repr__(self):
        return '<Obj id:{} value:{}>'.format(self.id, self.value)


def create_session_add_dummy_data():
    engine = create_engine('sqlite:///:memory:')
    session = Session(engine)
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)
    session.add(Obj(value=1))
    session.add(Obj(value=2))
    session.add(Obj(value=3))
    session.add(Obj(value=4))
    session.add(Obj(value=5))
    session.commit()
    return session


session = create_session_add_dummy_data()


class TestRepository(Base):
    __model__ = Obj
