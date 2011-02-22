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
LDAP
====

Access point storing items in an LDAP server.

"""

from __future__ import print_function
from kalamar.item import Item, MultiDict
from kalamar.access_point import AccessPoint
from kalamar.property import Property
from kalamar.request import Condition, And, Or, Not

try:
    import ldap
except ImportError:
    import sys
    print("WARNING: The LDAP AP is not available.", file=sys.stderr)
else:
    import ldap.modlist

class LdapItem(Item):
    """Item stored as a file."""
    @property
    def dn(self):
        """Distinguished name of the LDAP item."""
        return "cn=%s,%s" % (self["cn"],  self.access_point.ldap_path)


class LdapProperty(Property):
    """Property for an LDAP access point."""
    def __init__(self, rdn_name=None, **kwargs):
        super(LdapProperty, self).__init__(unicode, **kwargs)
        self.rdn_name = rdn_name
        self.name = None


class Ldap(AccessPoint):
    """Access point to an LDAP server."""
    ItemClass = LdapItem

    def __init__(self, hostname, ldap_path, user, password, properties, 
                 identity_properties=("cn",), encoding='utf-8'):
        if "cn" not in properties:
            raise KeyError("Properties list must contains a 'cn'")
        super(Ldap, self).__init__(properties, identity_properties)
        self.hostname = hostname
        self.encoding = encoding
        self.ldap_path = ldap_path
        self.ldap = ldap.open(hostname)
        self.ldap.simple_bind("%s,%s" % (user, ldap_path), password)
        for name, prop in self.properties.items():
            if prop.rdn_name is None:
                prop.rdn_name = name
            prop.name = name
    
    def _to_ldap_filter(self, condition):
        """Convert a kalamar condition to an LDAP filter."""
        if isinstance(condition, (And, Or, Not)):
            if isinstance(condition, Not):
                return "(! %s)" % self._to_ldap_filter(condition.sub_request)
            elif isinstance(condition, And):
                operator = "&"
            elif isinstance(condition, Or):
                operator = "|"
            return "(%s %s)" % (
                operator, " ".join(
                    self._to_ldap_filter(sub_condition) 
                    for sub_condition in condition.sub_requests))
        else:
            return "(%s%s%s)" % (
                condition.property, condition.operator, condition.value)

    def search(self, request):
        ldap_request = self._to_ldap_filter(request)
        for _, ldap_result in self.ldap.search_s(
            self.ldap_path, ldap.SCOPE_SUBTREE, ldap_request,
            # Restrict results to declared properties:
            [prop.rdn_name for prop in self.properties.values()]):
            multidict = MultiDict()
            for prop in self.properties.values():
                values = (
                    value.decode(self.encoding)
                    for value in ldap_result.get(prop.rdn_name, ()))
                multidict.setlist(prop.rdn_name, tuple(values) or (None,))
            yield self.create(multidict)
                    
    def delete(self, item):
        self.ldap.delete_s(item.dn)

    def save(self, item):
        modifications = {}
        for key in item:
            modifications[key] = tuple(
                value.encode(self.encoding) for value in item.getlist(key))
        old_entry = self.open(Condition("cn", "=", item["cn"]), None)
        if old_entry:
            self.ldap.modify_s(
                item.dn, ldap.modlist.modifyModlist(old_entry, modifications))
        else:
            self.ldap.add_s(item.dn, modifications.items())
