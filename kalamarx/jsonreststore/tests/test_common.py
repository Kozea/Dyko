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

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from nose.tools import eq_, nottest
from urllib import quote

import json

from kalamarx.jsonreststore.store import JSONRest
from functools import update_wrapper



@nottest
def commontest(test_function):
    '''
    Decorator to explicit a test which must run for all access sites. All the
    tests are saved in commontest.tests.
    '''
    test_function = nottest(test_function)
    commontest.tests.append(test_function)
    return test_function

commontest.tests = []

class testedsite(object):
    '''
    Decorator over a function that return an instance of site.

    The site must provide the following access_point:
        - test_ap : 
            * id: int (identity property)
            * color: unicode
            * name: unicode
            * foreign: many-to-one towards "foreign"
        - foreign : 
            * code : unicode (identity property)
            * name : unicode

    If that function meet the noses requirements to be tested, this
    site instance will be tested over all common tests.
    '''

    def __init__(self, teardown = None):
        """Teardown is a function accepting a kalamar site and tearing the test
        down"""
        self.teardown = nottest(teardown) if teardown is not None else None

    def __call__(self, make_site):
    
        def _run_test(site):
            """Returns a function executing the test given as argument
            against the site"""
            return lambda test : test(make_client(site))

            
        def test_run():
            """Run all tests"""
            for test in commontest.tests:
                site = make_site()
                runtest = _run_test(site)
                if self.teardown :
                    runtest.tearDown = lambda  : self.teardown(site) 
                yield runtest, test

        update_wrapper(test_run, make_site)

        return test_run

def make_client(kalamar_site):
    """Utility function creating a werkzeug client on a rest api"""
    application = JSONRest(kalamar_site)
    foreign_item1 = kalamar_site.create("foreign", {"code" : "AAA", "name":
    "Foreign AAA"})
    foreign_item1.save()
    foreign_item2 = kalamar_site.create("foreign", {"code" : "BBB", "name":
    "Foreign BBB"})
    foreign_item2.save()

    item = kalamar_site.create("test_ap", {'id': 1, 'name': 'Test one', 'color':
        'red', 'foreign' : foreign_item1})
    item.save()
    item = kalamar_site.create("test_ap", {'id': 2, 'name': 'Test two', 'color':
        'red', 'foreign': foreign_item2})
    item.save()
    item = kalamar_site.create("test_ap", {'id': 3, 'name': 'Test three',
        'color': 'blue', 'foreign': foreign_item1})
    item.save()
    item = kalamar_site.create("test_ap", {'id': 4, 'name': 'Test four',
        'color': 'green', 'foreign': None})
    item.save()
    item = kalamar_site.create("test_ap", {'id': 5, 'name': 'Test five',
        'color': 'blue', 'foreign': foreign_item2})
    item.save()
    return Client(application, BaseResponse)



def make_query(client, url, prefix="/test_ap/"):
    """Utility function allowing to jsonquery the rest api"""
    url = prefix + quote(url, safe="")
    resp = client.get(url)
    return json.loads(resp.data)

@commontest
def test_get_all(client):
    """Asserts that the get_all url is good"""
    items = make_query(client, "")
    eq_(len(items), 5)

@commontest
def test_get_all_order(client):
    """Assert that an order clause is working"""
    items = make_query(client, "[/color, \\name]")
    eq_(len(items), 5)
    #Assert that its sorted
    assert(all([a['color'] < b['color'] or
        (a['color'] == b['color'] and 
        a['name'] >= b['name'])
        for a, b in  zip(items[:-1],items[1:])]))

@commontest
def test_get_all_mapping(client):
    """Assert that mapping are working"""
    items = make_query(client, "[={foreign_name: foreign.name}]")
    eq_(len(items), 5)
    assert(all([a['foreign_name'] in [None, 'Foreign AAA', 'Foreign BBB']
            for a in items]))
    items = make_query(client, "[={id:id, label:name}]")
    eq_(len(items), 5)
    assert all(['id' in a and 'label' in a for a in items])

@commontest
def test_get_all_distinct(client):
    """Assert that a distinct is working"""
    items = make_query(client, "[={color: color}].distinct()")
    eq_(len(items), 3)

@commontest
def test_get_all_range(client):
    """Assert that range is working"""
    items = make_query(client, "[1:2]")
    eq_(len(items), 1)
    items = make_query(client, "[={color: color}].distinct()[/color][1:2]")
    eq_(len(items), 1)
    eq_(items[0]['color'], 'green')

@commontest
def test_get_all_filter(client):
    """Assert that various filters are working"""
    items = make_query(client, "[?id>3]")
    eq_(len(items), 2)
    items = make_query(client, '[?color!="blue"]')
    eq_(len(items), 3)
    items = make_query(client, '[?foreign.code = "BBB"]')
    eq_(len(items), 2)
    items = make_query(client, '[?color!="blue" & foreign.code="BBB"]')
    eq_(len(items), 1)
    items = make_query(client, '[?color!="blue" | foreign.code="BBB"]')
    eq_(len(items), 4)
    items = make_query(client, '[?id>3 & [color!="blue" | foreign.code="BBB"]]')
    eq_(len(items), 2)


@commontest
def test_get_item(client):
    """Test that a simple "getItem" is working"""
    items = make_query(client, "3")
    eq_(len(items), 1)


@commontest
def test_create_item(client):
    """Assert that an item can be created from the rest API"""
    foreign_item = make_query(client, 'BBB', "/foreign/")
    item = {"id" : 10, "name": "Test create", "color": "orangered",
            "foreign" : {"$ref" : "/foreign/BBB"}}
    item = json.dumps(item)
    client.post("/test_ap/", data = item)
    items = make_query(client, "10")
    eq_(len(items), 1)
    foreign_ref = items[0]["foreign"]["$ref"]
    foreign_item2 = json.loads(client.get(foreign_ref).data)
    eq_(foreign_item, foreign_item2)


@commontest
def test_update_item(client):
    """Assert that an item can be updated from the rest API"""
    foreign_item = make_query(client, '1')[0]
    foreign_item["name"] = "I'm updated"
    client.put("/test_ap/1", data = json.dumps(foreign_item))
    foreign_item = make_query(client, '1')[0]
    eq_(foreign_item["name"], "I'm updated")
    foreign_item["foreign"] = {"$ref": "foreign/AAA"}
    client.put("/test_ap/1", data = json.dumps(foreign_item))
    foreign_item = make_query(client, '1')[0]
    eq_(foreign_item["foreign"], {"$ref": "foreign/AAA"})

@commontest
def test_delete_item(client):
    """Assert that an item can be deleted from the rest API"""
    items = make_query(client, '')
    eq_(len(items), 5)
    assert 3 in [item['id'] for item in items]
    client.delete("/test_ap/3")
    items = make_query(client, '')
    eq_(len(items), 4)
    assert 3 not in [item['id'] for item in items]
