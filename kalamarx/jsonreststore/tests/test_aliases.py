# -*- coding: utf-8 -*-
# This file is part of Dykox
# Copyright © 2010 Kozea
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

from kalamar.access_point.aliases import Aliases
from kalamar.access_point.memory import Memory
from kalamar.property import Property
from kalamar.site import Site
from kalamar.item import Item
from .test_common import testedsite


@testedsite()
def test_aliases():
    """Returns a kalamar site containing aliased access_points"""
    remote_property = Property(Item, relation="many-to-one",
    remote_ap="foreign")
    underlying_ap = Memory({"id" : Property(int), "labeled_prop" :
        Property(unicode), "color": Property(unicode), "labeled_foreign" :
        remote_property}, ["id"])
    test_ap = Aliases(underlying_ap, {'name': 'labeled_prop', 'foreign':
    "labeled_foreign"})
    foreign_underlying_ap = Memory({"labeled_code": Property(unicode), "name":
        Property(unicode)},["labeled_code"])
    foreign_ap = Aliases(foreign_underlying_ap, {'code': 'labeled_code'})
    kalamar_site = Site()
    kalamar_site.register("test_ap", test_ap)
    kalamar_site.register("foreign", foreign_ap)
    return kalamar_site
