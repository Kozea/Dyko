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

from kalamar.access_point.alchemy import Alchemy, AlchemyProperty
from kalamar.site import Site
from kalamar.item import Item
from .test_common import testedsite

def tear_down(site):
    """Teardown method for the site.

    Drop every table
    """
    for access_point in site.access_points.values():
        access_point._table.drop()


@testedsite(tear_down)
def test_alchemy():
    """Test building the "standard test" kalamar site for alchemy"""
    url = "sqlite:///"
    remote_property = AlchemyProperty(Item, relation="many-to-one",
    remote_ap="foreign", remote_property="code", column_name="foreign")
    access_point = Alchemy(url, "test_ap", {
        "id": AlchemyProperty(int, column_name="id"),
        "name": AlchemyProperty(unicode, column_name="name"),
        "color": AlchemyProperty(unicode, column_name="color"),
        "foreign": remote_property},
        ["id"], True, engine_opts={'echo': True})
    foreign_access_point = Alchemy(url, "foreign", {
        "code": AlchemyProperty(unicode, column_name="code"),
        "name": AlchemyProperty(unicode, column_name="name")},
    ["code"], True)
    kalamar_site = Site()
    kalamar_site.register("test_ap", access_point)
    kalamar_site.register("foreign", foreign_access_point)
    return kalamar_site















