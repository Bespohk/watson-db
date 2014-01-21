# -*- coding: utf-8 -*-
from wsgiref import util
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from watson.framework import applications, events


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
        'default': {
            'connection_string': 'sqlite:///:memory:'
        }
    },
    'dependencies': {
        'definitions': {
            'sqlalchemy_declarative_base': {
                # bind to the instance of sqlalchemy_engine
                'item': lambda container: declarative_base(name='Model')
            },
        }
    },
    'events': {
        events.INIT: [
            ('watson.db.listeners.Init', 1, True)
        ],
    }
})


Model = app.container.get('sqlalchemy_declarative_base')


class Test(Model):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    value = Column(String(255))

engine = app.container.get('sqlalchemy_engine_default')
Model.metadata.drop_all(engine)
Model.metadata.create_all(engine)

session = app.container.get('sqlalchemy_session_default')

# Add some roles
session.add(Test(value=1))
session.add(Test(value=2))
session.add(Test(value=3))
session.add(Test(value=4))
session.add(Test(value=5))
session.commit()
