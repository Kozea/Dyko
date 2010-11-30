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

from nose.tools import eq_, nottest

from kalamarx.access_point.radicale import CalDav
from kalamar import Site 
from datetime import datetime
from tempfile import mkdtemp
from shutil import rmtree
import radicale
import time
from multiprocessing import Process

@nottest
def make_radicale(tempdir):
    """Starts a radical server, using the given folder"""
    radicale.ical.FOLDER = tempdir
    server = radicale.HTTPServer(("127.0.0.1", 5232),
        radicale.CalendarHTTPHandler)
    server.serve_forever()

APNAME = "mycalendar"


class TestRadicale(object):
    """Class testing the CalDav access point"""


    def setUp(self):
        """Sets the test up"""
        self.temp_dir = mkdtemp()
        print "TEMP: %s" % self.temp_dir
        self.start_radicale()
        self.site = self.make_site()

    def tearDown(self):
        """Tears the test down"""
        self.stop_radicale()
        rmtree(self.temp_dir)

    @nottest
    def start_radicale(self):
        """Start a radicale server in a separate process"""
        self.radicale_process = Process(target=make_radicale,
                args=(self.temp_dir,))
        self.radicale_process.start()
        time.sleep(0.1)

    @nottest 
    def stop_radicale(self):
        """Stop the radicale server"""
        self.radicale_process.terminate()
        time.sleep(0.1)


    @nottest
    def make_ap(self):
        """Creates the access point to be tested"""
        ap = CalDav('http://localhost:5232/radicale', ["calendar"])
        return ap

    @nottest
    def make_site(self):
        """Create the kalamar site to be tested"""
        site = Site()
        site.register(APNAME, self.make_ap())
        return site


    @nottest
    def assert_simple_item(self):
        """Utility method asserting that the calendar contains one and only one
        event"""
        items = list(self.site.search(APNAME,{}))
        print items
        eq_(len(items), 1)
        item = items[0]
        assert(item['uid'] is not None)
        return item

    @nottest
    def create_simple_item(self):
        """Utility method creating a simple item"""
        item = self.site.create(APNAME,{'dtstart' : datetime(2010, 9, 10, 12,
            00),
                            'dtend' : datetime(2010, 9, 10, 12, 00),
                            'dtstamp' : datetime(2010, 9, 24, 14, 30),
                            'created' : datetime.now(),
                            'uid' : None,
                            'calendar' : 'calendar',
                            'summary' : u'Kalamar supports caldav!',
                            'location' : u'Kozea Corp.'})
        item.save()
        return item


    def test_add_event(self):
        """Simple test asserting that an item can be created and properly
        saved"""
        self.create_simple_item()
        item = self.assert_simple_item()
        eq_(item['summary'], u'Kalamar supports caldav!')

    def test_remove_event(self):
        """Simple test asserting that an item can be properly deleted."""
        return
        self.create_simple_item()
        item = self.assert_simple_item()
        item.delete()
        items = list(self.site.search(APNAME))
        eq_(len(items), 0)

    def test_update_event(self):
        return
        """Simple test asserting that an item can be properly updated."""
        self.create_simple_item()
        item = self.assert_simple_item()
        item['summary'] = u'I AM UPDATED!'
        item.save()
        item = self.assert_simple_item()
        eq_(item['summary'], u'I AM UPDATED!')



