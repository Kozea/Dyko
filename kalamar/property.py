# -*- coding: utf-8 -*-
# This file is part of Dyko
# Copyright © 2008-2010 Kozea
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
Property
========

Kalamar property object.

"""

from .value import PROPERTY_TYPES, to_type
from .request import Condition
from .item import AbstractItem, Item



class MissingRemoteAP(RuntimeError):
    """Remote access point is missing in property definition."""
    value = __doc__


class MissingRemoteProperty(RuntimeError):
    """Remote property is missing in property definition."""
    value = __doc__


class AlreadyRegistered(RuntimeError):
    """Property is already registered so a site."""
    value = __doc__


class Property(object):
    """Access point property.

    :param property_type: Type of the property. Supported types are listed in
        :const:`value.PROPERTY_TYPES`. Additional types may work depending on
        the access point.
    :param boolean identity: Boolean defining if the property is identifying the
        item.
    :param auto: Function taking a :class:`Property` instance and returning a
        default value for the property.
    :param boolean mandatory: Boolean defining if the property is mandatory.
    :param relation: Type of the relation created by this property with another
        access point. Can be ``"many-to-one"``, ``"one-to-many"`` or ``None``.
    :param remote_ap: Remote access point linked by ``relation``.
    :param remote_property: Property of the remote access point linked by
        ``relation``.

    """
    def __init__(self, property_type, identity=False, auto=False,
                 mandatory=False, relation=None, remote_ap=None,
                 remote_property=None):
        self.type = property_type
        self.identity = identity
        self.auto = auto
        self.mandatory = mandatory
        self.relation = relation
        self._remote_ap_name = remote_ap
        self._remote_property_name = remote_property
        self.access_point = None
        self.name = None
        self.__remote_ap = None
        self.__remote_property = None

        # Raise an exception if something is wrong in the relation
        if self.relation and not self._remote_ap_name:
            raise MissingRemoteAP()
        if self.relation == "one-to-many" and not self._remote_property_name:
            raise MissingRemoteProperty()

    def bind(self, access_point, name):
        """Link the property to ``access_point`` and call it ``name``."""
        if not self.access_point and not self.name:
            self.access_point = access_point
            self.name = name
        else:
            raise AlreadyRegistered

    def cast(self, values):
        """Cast an iterable of values, return a tuple of cast values."""
        def cast_item(item_values):
            if item_values and item_values != (None,):
                for value in item_values:
                    if isinstance(value, AbstractItem):
                        yield value
                    else:
                        yield self.remote_ap.loader_from_reference_repr(unicode(value))(None)[0]
            else:
                yield None
        # DO NOT test for mandatory: when doing outer joins, a condition
        # can be None
        if values == (None,):
            return values
        if all(type(value) == self.type for value in values):
            return values
        # Ugly code to manage 'soft' references
        if self.relation == 'many-to-one':
            return tuple(cast_item(values))
        elif self.relation == 'one-to-many':
            #Assert that every value is an iterable of items
            return tuple(list(cast_item(value)) for value in values)
        elif self.type in PROPERTY_TYPES:
            return tuple(
                PROPERTY_TYPES[self.type](value) for value in values)
        else:
            return tuple(to_type(value, self.type) for value in values)

    def copy(self):
        """Return an empty copy of the property."""
        return Property(
            self.type, self.identity, self.auto, self.mandatory, self.relation,
            self._remote_ap_name, self._remote_property_name)

    @property
    def remote_ap(self):
        """Remote access point for linked properties."""
        if self.__remote_ap is None:
	        if self.access_point is not None and self._remote_ap_name:
                	access_points = self.access_point.site.access_points
                	self.__remote_ap = access_points.get(self._remote_ap_name)
        return self.__remote_ap

    @property
    def remote_property(self):
        """Remote property for linked properties."""
        if not self.__remote_property:
            if self.remote_ap:
                properties = self.remote_ap.properties
                self.__remote_property = properties[self._remote_property_name]
        return self.__remote_property
