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

"""This module provides a werkzeug converter to automatically parse JSONQueries

"""

from werkzeug.routing import BaseConverter , ValidationError
from kalamarx.jsonreststore.jsonqueryparser import parse
import logging


class KalamarRequestConverter(BaseConverter):
    """A werkzeug converter from JSONQuery to kalamar Query objects

    """
    regex = '\[.*'
    def __init__(self, url_map):
        super(KalamarRequestConverter, self).__init__(url_map)

    def to_python(self, value):
        try:
            value = parse(value)
            return value
        except:
            raise ValidationError
