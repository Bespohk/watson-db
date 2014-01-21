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
       'default': {
           'connection_string': 'sqlite:///:memory:',
           'engine_options': {},
           'session_options': {}
        }
    }

``engine_options`` and ``session_options`` are optional values and can
contain any kwarg values that ``create_session`` and ``sessionmaker``
take.

Example
-------

Once configured, the session can be retrieved from the container via
``container.get('sqlalchemy_session_[session name]')``.

watson.db also provides a paginator class for paginating a set of
results back from SQLAlchemy. Basic usage includes:

.. code-block:: python

        # within controller
        from watson.db import utils
        query = session.query(Model)
        paginator = utils.Pagination(query, limit=50)

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
