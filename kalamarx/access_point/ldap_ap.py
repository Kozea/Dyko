# -*- coding: utf-8 -*-
# This file is part of Dykox
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

"""This module provides an AccessPoint implementation to access a LDAP server
"""

from __future__ import print_function
from kalamar.item import MultiDict
from kalamar.access_point import AccessPoint
from kalamar.property import Property
from kalamar.request import Condition

try:
    import ldap
except ImportError:
    import sys
    print("WARNING: python-ldap module is not available.", file=sys.stderr)

class LdapProperty(Property):
    """Property for a Ldap access point."""
    def __init__(self, rdn_name=None, **kwargs):
        super(LdapProperty, self).__init__(unicode, **kwargs)
        self.rdn_name = rdn_name
        self.name = None


class Ldap(AccessPoint):
    """Access point to a LDAP server"""

    def __init__(self, hostname, ldap_path, user, password, properties, 
                 identity_properties=("cn",), encoding='utf-8'): 
        super(Ldap, self).__init__(properties, identity_properties)
        self.hostname = hostname
        self.encoding = encoding
        self.ldap_path = ldap_path
        self.ldap = ldap.open(hostname)
        self.ldap.simple_bind(user + "," + ldap_path, password)
        for name, prop in self.properties.items():
            if prop.rdn_name is None:
                prop.rdn_name = name
            prop.name = name
    
    def search(self, request):
        """Return an iterable of every item matching request."""
        ldap_request = "%s%s%s" % (
            request.property, request.operator, request.value)
        for _, ldap_result in self.ldap.search_s(
            self.ldap_path, ldap.SCOPE_SUBTREE, ldap_request):
            multidict = MultiDict()
            for prop in self.properties.values():
                multidict.setlist(
                    prop.rdn_name, 
                    tuple(ldap_result.get(prop.rdn_name, (None,))))
            yield self.create(multidict)
                    
    def delete(self, item):
        """Delete ``item`` from the Ldap."""
        ident = "cn=%s,%s" % (item["cn"],  self.ldap_path)
        print(ident)
        print(ident)
        self.ldap.delete_s(ident)

    def save(self, item):
        """Update or add the item."""
        ident = "cn=%s,%s" % (item["cn"],  self.ldap_path)
        modlist = []
        for key in item.keys():
            values = item.getlist(key)
            new_values = []
            for value in values:
                new_values.append(value.encode(self.encoding))
            modlist.append((key, tuple(new_values)))
        print(modlist)
        old_entry = self.open(Condition("cn", "=", item["cn"]), None)
        if old_entry:
            self.ldap.modify_s(
                ident, ldap.modlist.modifyModlist(old_entry, dict(modlist)))
        else:
            self.ldap.add_s(ident, modlist)
 


    
