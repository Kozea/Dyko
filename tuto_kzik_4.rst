=========
Chapter 4
=========
Design your flow pages 

- Define rules
- Define controlleurs
- Define utilities of project

.. contents::

Flow of pages
=============
Now add new lines in your file urls.py. Each rule define the link logic with its handlerequest in controller main.py.

urls.py::

  from werkzeug.routing import Map, Rule

  map = Map()

  _default_rules = (
      Rule('/musik/<string:artistname>/<string:albumname>/<string:name>', endpoint='remote'),
      Rule('/static/<path:path>', endpoint='static_file'),
      Rule('/<any(index,about_us):template>', endpoint='simple_template'),
      Rule('/<any(artistslist):template>', endpoint='artistslist_template'),
      Rule('/<any(albumslist):template>', endpoint='albumslist_template'),
      Rule('/<any(trackslist):template>', endpoint='trackslist_template'),
      Rule('/<string:artistname>/<string:albumname>/<string:name>', endpoint='player_template'),
      Rule('/<string:artistname>/<string:albumname>', endpoint='trackslist_template'),
      Rule('/<string:artistname>', endpoint='albumslist_template'),
      Rule('/', endpoint='simple_template')
      )

  for rule in _default_rules:
      map.add(rule)

Utilities
=========

helpers/helpers.py::

  from .. import kalamar

  def sort_album(tracks):
      return sorted(tracks, key=lambda track: int(track["track"]))

  def url_to_item(artistname,albumname,name):
      return kalamar.open(
          "track", {"artist": artistname, "album": albumname, "name": name})

Hanlde request
==============

controller/main.py::

  import os.path
  from kraken.utils import StaticFileResponse, NotFound

  from ..helpers import helpers

  def _static(filename):
      if not os.path.isfile(filename):
          raise NotFound
      return StaticFileResponse(filename)

  def simple_template(request, template="index" , **data):
      template_path = os.path.join(
              request.kraken.site_root, "views", "%s.html.jinja2" % template)    
      return request.template_response(template_path, data)

  def player_template(request, **data):
      template="player"
      template_path = os.path.join(
              request.kraken.site_root, "views", "%s.html.jinja2" % template)
      return request.template_response(template_path, data)

  def trackslist_template(request, **data):
      template="trackslist"
      if "artistname" not in data:
          data["artistname"]="all"
      if "albumname" not in data:
          data["albumname"]="all"
      template_path = os.path.join(
              request.kraken.site_root, "views", "%s.html.jinja2" % template)
      return request.template_response(template_path, data)

  def albumslist_template(request, **data):
      template="albumslist"
      if "artistname" not in data:
          data["artistname"]="all"
      template_path = os.path.join(
              request.kraken.site_root, "views", "%s.html.jinja2" % template)
      return request.template_response(template_path, data)

  def artistslist_template(request, **data):
      template="artistslist"
      template_path = os.path.join(
              request.kraken.site_root, "views", "%s.html.jinja2" % template)
      return request.template_response(template_path, data)

  def static_file(request, path):
      path = request.path.strip('/')
      filename = os.path.join(request.kraken.site_root, path)
      return _static(filename)

  def remote(request, artistname,albumname,name):
      item = helpers.url_to_item(artistname,albumname,name)
      return StaticFileResponse(item.filename)


