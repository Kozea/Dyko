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

from kalamar.access_point import AccessPoint
from kalamar.property import Property
from kalamar.request import Condition
from collections import OrderedDict
import urllib, json, pickle

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
        self.persistent_file = persistent_file
        if persistent_file is None:
            self._cache = {}
        else:
            fd = open(persistent_file)
            self._cache = OrderedDict(pickle.load(fd))

    def search(self, request):
        if not (isinstance(request, Condition)
                and request.property.name == "address"):
            raise NotImplementedError(
                "Only simple search on 'address' is currently supported")
        address = request.value.encode("utf-8")
        results = self._cache.get(address, None)
        if results is not None:
            self.site.logger.debug("Got address %s from cache", address)
        else:
            self.site.logger.info("Searching address %s from google geocoding API", address)
            json_results = json.loads(
                urllib.urlopen(
                    API_URL + urllib.quote(
                        address)).read())
            if json_results["status"] not in ("OK", "ZERO_RESULTS"):
                raise GeocoderException(json_results["status"])
            results = [{
                    "address": request.value,
                    "lat": json_result["geometry"]["location"]["lat"],
                    "lng": json_result["geometry"]["location"]["lng"]
                    } for json_result in json_results["results"]]
            self._cache[address] = results
            if self.persistent_file:
                fd = open(self.persistent_file, 'w')
                pickle.dump(self._cache, fd)
                fd.close()
        for result in results:
            yield self.create(result)

    def delete(self, item):
        raise NotImplementedError("Read only access point")

    def save(self, item):
        raise NotImplementedError("Read only access point")
