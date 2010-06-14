=========
Chapter 1
=========

.. contents::

The Folder structure
====================

::

  kzik.py
  dispatcher.py
  urls.py
  kzik.conf
  views/
  static/
  helpers/
    __init__.py
  controllers/
    __init__.py
    main.py

- kzik.py : Execute the site
- dispatcher.py : A configurable dispatcher which dispatch requests between different modules
- kzik.conf : Define business logic of project
- urls.py : A rules list used by  dispatcher
- controllers/main.py : functions who handle requests defined in urls
- helpers : common utils used in projetct
- views: pagewebs where user interacts with by using a template engine(Jinja2 in this project)

Controllers and views creation
==============================

Routing rules
-------------
urls.py::

  from werkzeug.routing import Map, Rule

  map = Map()

  _default_rules = [
      Rule('/', endpoint='simple_template')
      ]

  for rule in _default_rules:
      map.add(rule)

Controllers creation
--------------------
main.py::

  import os.path

  def simple_template(request, template="index" , **data):
      #Return view corresponding to client request
      template_path = os.path.join(
              request.kraken.site_root, "views", "%s.html.jinja2" % template)
      return request.template_response(template_path, data)

Views creation
--------------

index.html.jinja2 in views/::

  Hello world!

Launch server
=============

Create WSGI application Kzik site and kalamar configuration
-----------------------------------------------------------

kzik.py::

  import kraken
  class Site(kraken.Site):
      def handle_request(self, request):
          return self.import_('dispatcher').dispatch(request)
  application = Site(site_root='.', kalamar_conf='./kzik.conf')
  #launch the localhost
  kraken.runserver(application)

Handle request
--------------

dispatcher.py::

  from . import urls
  from .controllers import main as controllers

  def dispatch(request):
      url_map = urls.map.bind_to_environ(request.environ)
      # Raises a HttpException catched by kraken for 404s and redirects
      endpoint, kwargs = url_map.match()
      return getattr(controllers, endpoint)(request, **kwargs)

Launch server
-------------
To run your application, execute this command from your command line ::

  ./kzik.py

  * Running on http://localhost:5000/

Now open your broswer, you can view 'Hello world!'
