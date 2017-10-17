Usage
=====

Configuration
-------------

Before being able to integrate SqlAlchemy with Watson, there are a few
things that must be implemented first within your applications config.

1. Add the init event to your applications configuration.

.. code-block:: python

   'events': {
        events.INIT: [
            ('watson.db.listeners.Init', 1, True)
        ],
    }

2. Create a default configuration for a database session.

.. code-block:: python

   db = {
       'connections': {
         'default': {
             'connection_string': 'sqlite:///:memory:',
             'engine_options': {},
             'session_options': {}
          }
        }
    }

``engine_options`` and ``session_options`` are optional values and can
contain any kwarg values that ``create_session`` and ``sessionmaker`` from SqlAlchemy take.

A full example configuration might look like this:

.. code-block:: python

    db = {
       'connections': {
            'default': {
                'connection_string': 'sqlite:///../data/db/default.db',
                'metadata': 'app.models.Model',
                'engine_options': {
                    'encoding': 'utf-8',
                    'echo': False,
                    'pool_recycle': 3600
                }
            },
        },
        'migrations': {
            'path': '../data/db/migrations',
            'use_twophase': False
        },
        'fixtures': {
            'path': '../data/db/fixtures',
            'data': (
                # Fixtures will be located in ../data/db/fixtures/model.json
                # and will be inserted into the 'default' database.
                ('model', None),
            )
        }
    }

Fixtures
--------

Fixtures are a way of inserting some initial data into a database to populate it. They are stored in basic JSON format, and can be defined as follows.

.. code-block:: javascript

    [
        {
            "class": "app.models.Model",
            "fields": {
                "id": 1,
                "column": "Value"
            }
        }
        // .. more records
    ]

Each fixture that is to be loaded via the `populate` command should be included in the ``data`` value of the ``fixtures`` in the format ``(FIXTURE_NAME, DATABASE_CONNECTION_NAME)``. If DATABASE_CONNECTION_NAME is set to None, then the default connection will be used.

Migrations
----------

Watson DB utilizes Alembic to handle migrations, which can be run via the command line. See the commands section of this document for more information on the individual commands.

Commands
--------

The commands available to you are split into two namespaces, db, and db:migrate. These can be accessed via ``./console.py db`` and ``./console.py db:migrate`` respectively.

db
^^

*create*

Creates the databases against the associated model metadata and connections.

*dump*

Prints out the SQL statements used to create the database.

*populate*

Inserts the data from the fixtures into the databases.

db:migrate
^^^^^^^^^^

These commands are essentially wrappers to the Alembic command line. Additional arguments that can be specified can be found by appending --help to the command.

*branches*

*current*

*downgrade*

*history*

*init*

*revision*

*stamp*

*upgrade*


Services
--------

Services provide a straightforward way to interact with the models in your application without having to directly call against the SqlAlchemy session itself. Each service should be defined within the configuration to use the relevant SqlAlchemy session in it's constructor.

.. code-block:: python

    dependencies = {
        'definitions': {
            'myservice': {
                'item': 'myapp.services.MyService',
                'init': ['sqlalchemy_session_default']
            },
            'mycontroller': {
                'item': 'myapp.controllers.MyController',
                'property': {
                    'service': 'myservice'
                }
            }
        }
    }

Example
-------

Once configured, the session can be retrieved from the container via
``container.get('sqlalchemy_session_[SESSION_NAME]')``.

watson.db also provides a paginator class for paginating a set of
results back from SQLAlchemy. Basic usage includes:

.. code-block:: python

        # within myapp.models
        from watson.db import models

        class MyModel(models.Model):
            # .. columns

        # within myapp.services
        from watson.db import services
        from myapp import models

        class MyService(services.Base):
            __model__ = models.MyModel

        # within myapp.controllers, assuming the MyService object has
        # been injected into the controller as the `service` attribute.
        from watson.db import utils
        from watson.framework import controllers

        class MyController(controllers.Rest):
            def GET(self):
                return {
                    'paginator': utils.Pagination(self.service.query, limit=50)
                }

.. code-block:: html

        # within view
        {% for item in paginator %}
        {% endfor %}
        <div class="pagination">
        {% for page in paginator.iter_pages() %}
            {% if page == paginator.page %}
            <a href="#" class="current">{{ page }}</a>
            {% else %}
            <a href="#">{{ page }}</a>
            {% endif %}
        {% endfor %}
        </div>
