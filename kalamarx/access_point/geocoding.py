# -*- coding: utf-8 -*-
# This file is part of Dyko
# Copyright © 2011 Kozea
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

"""
Geocoding
====

Read only access point to get longitude and latitude 
from the `Google geocoding API<http://code.google.com/apis/maps/documentation/geocoding/>`_

Please read and respect `the terms of services<http://code.google.com/apis/maps/terms.html#section_10_12>`_

"""

from __future__ import print_function
from kalamar.access_point import AccessPoint
from kalamar.property import Property
from kalamar.request import Condition
import urllib, json, shelve

API_URL="http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address="

class GeocoderException(Exception):
    pass

class Geocoder(AccessPoint):
    """Access point to a Google Geocoding API.

    If you want the geocode cache to be persistent, set persistent_file 
    to a file path
"""

    def __init__(self, persistent_file=None):
        properties = {
            "address": Property(unicode),
            "lat": Property(float),
            "lng": Property(float),
            }
        identity_properties = ("address",)
        super(Geocoder, self).__init__(properties, identity_properties)
        if persistent_file is None:
            self._cache = {}
        else:
            self._cache = shelve.open(persistent_file)

    def search(self, request):
        if not (isinstance(request, Condition) 
                and request.property.name == "address"):
            raise NotImplementedError(
                "Only simple search an 'address' is currently supported")
        
        results = self._cache.get(request.value.encode("utf-8"), None)
        if results:
            print("From cache")
        if not results:
            print("From net")
            json_results = json.loads(
                urllib.urlopen(API_URL + urllib.quote(request.value.encode("utf-8"))).read())
            if json_results["status"] not in ("OK", "ZERO_RESULTS"):
                raise GeocoderException(json_results["status"])
            results = [{
                    "address": request.value,
                    "lat": json_result["geometry"]["location"]["lat"],
                    "lng": json_result["geometry"]["location"]["lng"]
                    } for json_result in json_results["results"]]
            self._cache[request.value.encode("utf-8")] = results
            if type(self._cache) != dict:
                self._cache.sync()
        for result in results:
            yield self.create(result)
                    
    def delete(self, item):
        raise NotImplementedError("Read only access point")

    def save(self, item):
        raise NotImplementedError("Read only access point")
        
