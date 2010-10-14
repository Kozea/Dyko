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

"""This module offers a jsonquery parser, producing kalamar Query objects

"""

# pylint: disable=C0103
import ply.yacc as yacc
from kalamarx.jsonreststore.jsonquerylexer import tokens
from kalamar.request import Condition
from kalamar import query

def p_composed_query(p):
    ''' query : query query
    '''
    p[0] = query.QueryChain([p[1], p[2]])


#Define the "queries"
def p_query(p):
    ''' query : condition
            |   order 
            |   select
            |   distinct
            |   range
            '''
    p[0] = p[1]


def p_distinct(p):
    ''' distinct : query DISTINCT'''
    p[0] = query.QueryChain([p[1], query.QueryDistinct()])


#Define the condition parser
def p_condition(p):
    ''' condition : SUBEXPRESSION_START CONDITION_SYMBOL test SUBEXPRESSION_END
                '''
    p[0] = query.QueryFilter(p[3])

def p_complex_condition(p):
    ''' test : SUBEXPRESSION_START test SUBEXPRESSION_END '''
    p[0] = p[2]

def p_bin_expr_cond(p):
    '''test : test BIN_OPERATOR test '''
    p[0] = p[2](p[1], p[3])

#def p_condition_simple(p):
#    '''condition : test'''
#    p[0] = p[1]

def p_expression_cond(p):
    '''test : PROPERTY OPERATOR scalar '''
    p[0] = Condition(property_name = p[1], operator = p[2], value = p[3])


#Define the sort parser
def p_sort(p):
    ''' sortgroup : SORT PROPERTY '''
    p[0] = [(p[2], p[1])]

def p_sort_group(p):
    ''' sortgroup : sortgroup LIST_SEPARATOR sortgroup
    '''
    p[1].extend(p[3])
    p[0] = p[1]


def p_order_expression(p):
    ''' order : SUBEXPRESSION_START sortgroup SUBEXPRESSION_END '''
    p[0] = query.QueryOrder(p[2])


#Base elements for conditions
def p_scalar(p):
    ''' scalar :     STRING
                |    NUMBER '''
    p[0] = p[1]

#Define mapping parser

def p_select(p):
    ''' select : MAPPING_START aliases SUBEXPRESSION_END 
    '''
    p[0] = query.QuerySelect(p[2])

def p_select_single(p):
    ''' select : MAPPING_START PROPERTY SUBEXPRESSION_END '''
    p[0] = query.QuerySingleSelect(p[2])

def p_aliases(p):
    ''' aliases : DICT_START alias_group DICT_END '''
    p[0] = p[2]

def p_mapping_group(p):
    ''' alias_group : alias_group LIST_SEPARATOR alias_group '''
    p[1].update(p[3])
    p[0] = p[1]

def p_mapping(p):
    ''' alias_group : PROPERTY MAPPING_DELIMITOR PROPERTY'''
    p[0] = dict([(p[1], p[3])])


def p_range(p):
    ''' range : SUBEXPRESSION_START NUMBER  \
            MAPPING_DELIMITOR NUMBER SUBEXPRESSION_END '''
    p[0] = query.QueryRange(slice(p[2], p[4]))

yacc.yacc(debug=True)

def parse(query_string):
    """Parses a query string
    >>> import itertools
    >>> items = itertools.cycle([{'a':1, 'b':1},{'a':2, 'b': 2}]) 
    >>> query = parse("[?a=2][1:3]")
    >>> list(query(items))
    [{'a': 2, 'b': 2}, {'a': 2, 'b': 2}]
    >>> query = parse("[?a=2][1:3].distinct()")
    >>> list(query(items))
    [{'a': 2, 'b': 2}]
    >>> items = [{"a" : 4, "b" : 8}, {"a" : 5 , "b" : 7}, {"a" : 5, "b" : 8}]
    >>> query = parse("[/a,\\\\b]")
    >>> list(query(items))
    [{'a': 4, 'b': 8}, {'a': 5, 'b': 8}, {'a': 5, 'b': 7}]
    >>> query = parse("[? a=4 | [a=5 & b=8]]")
    >>> list(query(items))
    [{'a': 4, 'b': 8}, {'a': 5, 'b': 8}]
    >>> items = [{"a" : {'id': 1, 'label': 'test'}, "id" : 8}, {"a": {'id': 2}}]
    >>> query = parse("[?a.id=1][={label:a.label, id:id, truc:a.id}]")
    >>> list(query(items))
    [{'truc': 1, 'id': 8, 'label': 'test'}]
    """

    return yacc.parse(query_string)
