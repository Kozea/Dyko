===============
 Documentation
===============

.. contents::


Installation
============

Using PyPI
----------

Dyko is `available on PyPI <http://pypi.python.org/pypi/Dyko/>`_. To install,
just type as superuser::

  easy_install dyko

Using sources
-------------

Download the `git master or the sources tarball </download>`_, and install Dyko
by typing in a terminal, as superuser::

  python setup.py install

Dependences
-----------

Dyko has a few optional dependences:

- `Werkzeug <http://werkzeug.pocoo.org/>`_, web server needed for Kraken;
- `Jinja2 <http://jinja.pocoo.org/>`_, `Mako <http://www.makotemplates.org/>`_
  and `Genshi <http://genshi.edgewall.org/>`_, 3 templates engines, useful to
  chose one if you want to write dynamic HTML pages with Kraken;
- `SQLAlchemy <http://www.sqlalchemy.org/>`_, needed for managing databases in
  Kalamar;
- `lxml <http://codespeak.net/lxml/>`_, needed for managing XML in Kalamar;
- `docutils <http://docutils.sourceforge.net/>`_, needed for managing
  ReStructuredText in Kalamar.


API
===

You can read the API documentation for:

- `Kalamar </static/api/kalamar.html>`_, the content management library;
- `Kraken </static/api/kraken.html>`_, the HTTP request and template manager.


Howto
=====

Create a simple website
-----------------------

Quick and dirty website in 1 minute::

  $ easy_install Dyko, Werkzeug, Jinja2
  $ mkdir website
  $ cd website
  $ mkdir views
  $ cat "<h1>Hello world</h1>" > views/hello.html.jinja2
  $ python
  >>> from kraken import runserver, site
  >>> runserver(site.Site())

Then open http://localhost:5000/hello in a browser.

If you want to go further, just `get started </tutorials/Getting%20started>`_.

Use multiple template engines
-----------------------------

In your folder containing the views, the files should have two extensions. The
first one is used for mimetype, the second one for the template engine. A file
called ``hello.html.jinja2`` will be (by default) available at the ``/hello``
URL, with a ``text/html`` mimetype, parsed by the Jinja2 template engine.

You can learn `more about template engines
</static/api/kraken.html#template-engine>`_ in our API documentation.
