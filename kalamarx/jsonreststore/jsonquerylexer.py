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

"""This module provides a jsonquery lexer

    See http://docs.persvr.org/documentation/jsonquery 
"""
# pylint: disable=C0103
import ply.lex as lex
import sys

from kalamar.request import And, Or

tokens = (
    'SUBEXPRESSION_START',
    'SUBEXPRESSION_END',
    'NUMBER',
    'OPERATOR',
    'PROPERTY_ID',
    'STRING_DOUBLE_QUOTE',
    'STRING_SINGLE_QUOTE',
    'BIN_OPERATOR',
    'SORT',
    'LIST_SEPARATOR',
    'CONDITION_SYMBOL',
    'MAPPING_START',
    'MAPPING_DELIMITOR',
    'DISTINCT',
    'PROPERTY_SEPARATOR',
    'DICT_START',
    'DICT_END',
    'CURRENT_OBJECT',
    'LEFT_PAREN',
    'RIGHT_PAREN'
)

t_DISTINCT = r'\.distinct\(\)'

t_LEFT_PAREN = '\('
t_RIGHT_PAREN = '\)'

t_SUBEXPRESSION_START = r'\['

t_SUBEXPRESSION_END = r'\]'

t_MAPPING_START = r'\[='
t_MAPPING_DELIMITOR = r':'

t_DICT_START = r'{'
t_DICT_END = r'}'

t_PROPERTY_SEPARATOR = r'\.'

t_LIST_SEPARATOR = r','

t_ignore = '\t\n '

t_CONDITION_SYMBOL = '\?'

t_CURRENT_OBJECT = '@'

BIN_OPS = {'&': And, '|': Or}
SORT = { '\\' : False, '/': True}

def t_SORT(t):
    r'[/\\]'
    t.value = SORT[t.value]
    return t

def t_STRING_DOUBLE_QUOTE(t):
    r'"[^"]+"'
    t.value = t.value[1:-1]
    return t

def t_STRING_SINGLE_QUOTE(t):
    r"'[^']+'"
    t.value = t.value[1:-1]
    return t


def t_OPERATOR(t):
    r'[=><]|<=|>=|!=|~'
    t.value = t.value
    return t

def t_NUMBER(t):
    r'\d+|([Ii]nfinity)'
    if str(t.value).lower() == 'infinity':
        t.value = None
    else:
        t.value = int(t.value)
    return t


def t_PROPERTY_ID(t):
    r'(@\.)?([a-zA-Z_]+[a-zA-Z\d_]*)+(\.([a-zA-Z_]+[a-zA-Z\d_]*))*'
    t.value = str(t.value).strip('@.')
    return t


def t_BIN_OPERATOR(t):
    r'[&|]'
    t.value = BIN_OPS[t.value]
    return t

lex.lex()
