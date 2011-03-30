# -*- coding: utf-8 -*-
# This file is part of Dyko
# Copyright © 2008-2009 Kozea
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Kalamar.  If not, see <http://www.gnu.org/licenses/>.

"""A JSONRest API for Kalamar.

See http://docs.dojocampus.org/dojo/store/JsonRest for a more complete 
definition

"""


# pylint: disable=F0401
try:
    import json
except ImportError:
    import simplejson as json
# pylint: enable=F0401

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import NotFound
from werkzeug.urls import url_unquote
from kalamar.item import AbstractItem
from kalamar.query import QueryChain
from kalamar.value import Iter
from decimal import Decimal
from datetime import date
from kalamarx.jsonreststore.requestconverter import KalamarRequestConverter



class KalamarJSONDecoder(json.JSONDecoder):
    """Custom JSONDecoder wich automatically fetches the references."""

    def __init__(self, restapi=None, **kwArgs):
        self.restapi = restapi
        super(KalamarJSONDecoder, self).__init__(object_hook = self._decoder)

    def _decoder(self, value):
        """Decoder given to the standard JSONDecoder"""
        if hasattr(value, "__iter__") and "$ref" in value:
            ref = value["$ref"]
            if ref.startswith("/"):
                ref = ref[1:]
            return self.restapi.ref_to_item(ref)
        else :
            return value







class KalamarJSONEncoder(json.JSONEncoder):
    """Encode python objects to json consumable by dojo.

    """
    def __init__(self, **kwArgs):
        super(KalamarJSONEncoder, self).__init__(self, default = self._encoder)

    def _encoder(self, obj):
        """Default implementation adding support for date, set, Decimal and
        item

        """
        jsonvalue = "null"
        if isinstance(obj, (set, tuple, Iter)):
            jsonvalue = list([self.default(value) for value in obj])
        elif isinstance(obj, Decimal):
            jsonvalue = str(obj)
        elif isinstance(obj, date):
            jsonvalue = {"_type":"Date", "_value":obj.isoformat()}
        elif isinstance(obj, AbstractItem):
            ap_name = obj.access_point.name
            ap_properties = obj.access_point.identity_properties
            jsonvalue = {"$ref": "%s/%s" % (ap_name, "/".join([str(obj[prop.name])
                for prop in ap_properties]))}
            return jsonvalue
        else :
            jsonvalue = json.dumps(obj)
        return jsonvalue

def tojson(an_object):
    """ Returns a json representation from an object"""
    return json.dumps(an_object, cls=KalamarJSONEncoder)



class JSONRest:
    """WSGI application exposing a kalamar site as a JsonREST service.

    """

    def __init__(self, kalamar_site, base_url="", wrapped_app = None):
        self.kalamar = kalamar_site
        self.wrapped_app = wrapped_app
        self.url_map = Map([
                    Rule('%s/<string:access_point>/<request:query>' % base_url,
                        methods=("GET",), endpoint = "get_all"),
                    Rule('%s/<string:access_point>/' % base_url,
                        methods=("GET",), defaults={'query':
                            QueryChain([])},  endpoint = "get_all"),
                    Rule('%s/<path:ref>' % base_url,
                        methods= ("GET",), endpoint = "get_item"),
                    Rule('%s/<path:ref>' % base_url,
                        methods=("PUT",), endpoint = "save_item"),
                    Rule('%s/<path:ref>' % base_url,
                        methods=("DELETE",), endpoint = "delete_item"),
                    Rule('%s/<string:access_point>/' % base_url,
                        methods=("POST",), endpoint = "create_item")
            ], converters={"request" : KalamarRequestConverter})

    def __call__(self, environ, start_response):
        if environ['QUERY_STRING']:
            environ['PATH_INFO'] = '%s?%s' % (environ['PATH_INFO'],
                    url_unquote(environ['QUERY_STRING']))
        request = Request(environ)
        url_map = self.url_map.bind_to_environ(request.environ)
        try :
            endpoint, kwargs = url_map.match()
            if request.data:
                kwargs['data'] = self.fromjson(request.data)
            if 'ref' in kwargs:
                kwargs['item'] = self.ref_to_item(kwargs.pop('ref'))
            handler = getattr(self, endpoint)
            response = handler(**kwargs)
            return response(environ, start_response)
        except NotFound as e:
            if self.wrapped_app:
                return self.wrapped_app(environ, start_response)
            else:
                return e(environ, start_response)



    def __get_access_point(self, access_point):
        """Returns an access point from its name
        """
        return self.kalamar.access_points[access_point]


    def get_item(self, item):
        """GET API returning a unique item encoded in json

        """
        return JSONResponse([dict(item)])

    def save_item(self, data, item):
        """Saves an item
        """
        for prop_name, value in data.items():
            if prop_name not in [prop.name for prop in item.access_point.identity_properties]:
                item[prop_name] = value
        item.save()
        return JSONResponse(item)

    def delete_item(self, item):
        """Deletes an item
        """
        item.delete()
        return JSONResponse([])

    def get_all(self, access_point, query):
        """Performs a "view" request on an access point

        """
        return JSONResponse(list(self.kalamar.view(access_point, query=query)))

    def create_item(self, access_point, data):
        """Create and save a new item

        """
        item = self.kalamar.create(access_point, data)
        item.save()
        return JSONResponse(item)


    def fromjson(self, an_object):
        """ Returns a python representation from a jsonstring"""
        return json.loads(an_object, cls=KalamarJSONDecoder,
                restapi=self)

    def ref_to_item(self, ref):
        identity = ref.split("/")
        access_point = identity[0]
        id_properties = [prop.name for prop in self.kalamar.access_points[access_point].\
                identity_properties]
        request = dict(zip(id_properties, identity[1:]))
        return self.kalamar.open(access_point,
                request)


class JSONResponse(Response):
    """Represents an http response suitable for transporting JSON

    """
    def __init__(self, content, headers = None):
        super(JSONResponse, self).__init__(self)
        self.content = tojson(content)
        self.headers = headers or []
        self.headers.extend((('Content-type', 'application/json'),
                       ('Content-Length', str(len(self.content)))))

    def __call__(self, environ, start_response):
        start_response('200 OK', self.headers)
        return self.content
