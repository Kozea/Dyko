=============
Project Kazik
=============

The Kzik project is an online music manager. The purpose os this tutorial is to introduce the different steps allowing to create this manager.

.. contents::
Installation
============
Before starting this tutorial, please read the documentation about how to install dyko.

``link``

The Folder structure
====================

::

  kzik.py
  dispatcher.py
  urls.py
  controllers/
    __init__.py
    main.py
  helpers/
  views/
  static/

- kzik.py : to create the site
- dispatcher.py : A configurable dispatcher which dispatch requests between different modules.
- urls.py : a rules list used by  dispatcher.
- controllers/main.py : functions who handle requests defined in urls
- helpers : common utils used in projetct
- views: pagewebs where user interacts with by using a template engine(Jinja2 in this project) 

Controllers and views creation
==============================

  werkzeug link  

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

  hello world

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

In your browser, you can read 'hello world'

Data Structure
==============

An example of data structure::

  /
  home/
    music/
      artist/
        album/
          track01 - name1.mp3
          track02 - name2.ogg
          ...

- In the file configuration of Kzik, 
- In "url", we define place where music is stored
- In "filename_format", indicate the logic format of the music content
- In "storage_aliases", give aliases

kzik.conf::

  [track]
  url: file:///home/music
  filename_format: */*/* - *.*
  storage_aliases: artist=path1/album=path2/track=path3/name=path4/format=path5








