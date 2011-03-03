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
import urllib, json

API_URL="http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address="

class GeocoderException(Exception):
    pass

class Geocoder(AccessPoint):
    """Access point to a Google Geocoding API."""

    def __init__(self):
        properties = {
            "address": Property(unicode),
            "lat": Property(float),
            "lng": Property(float),
            }
        identity_properties = ("address",)
        super(Geocoder, self).__init__(properties, identity_properties)

    def search(self, request):
        if not (isinstance(request, Condition) 
                and request.property.name == "address"):
            raise NotImplementedError(
                "Only simple search an 'address' is currently supported")

        results = json.loads(
            urllib.urlopen(API_URL + urllib.quote(request.value)).read())
        if results["status"] not in ("OK", "ZERO_RESULTS"):
            raise GeocoderException(results["status"])
        
        for result in results["results"]:
            yield self.create({
                    "address": request.value,
                    "lat": result["geometry"]["location"]["lat"],
                    "lng": result["geometry"]["location"]["lng"]
                    })
                    
    def delete(self, item):
        raise NotImplementedError("Read only access point")

    def save(self, item):
        raise NotImplementedError("Read only access point")
        
