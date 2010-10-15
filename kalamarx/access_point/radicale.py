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

"""This module provides an AccessPoint implementation to access a radicale
CalDavServer
"""


from kalamar.item import Item 
from caldav import DAVClient, Calendar, Event
from datetime import datetime
from kalamar.access_point import AccessPoint 
from kalamar.property import Property


class CalDav(AccessPoint):
    """Access point to a caldav server
    
       The access point is meant to map to a single Calendar.
       The items returned represents events from within the calendar

    """

    event_properties = {
        "dtstart": Property(datetime),
        "dtend": Property(datetime),
        "dtstamp": Property(datetime),
        "created": Property(datetime),
        "uid": Property(unicode),
        "x-radicale-name": Property(unicode),
        "summary": Property(unicode),
        "location": Property(unicode),
        "rrule" : Property(unicode),
        "description" : Property(unicode),
        "sequence": Property(int)
    }


    def __event_to_item_dict(self, event):
        """Converts an event from the caldav library to a dict
        
        """
        values = []
        for prop in self.properties:
            event_property = event.instance.vevent.contents.get(prop)
            values.append((prop, event_property[0].value 
                if event_property else None))
        return dict(values)

    def __make_calendar(self, calendar):
        """Returns a calendar object from a calendar name
        
        """
        return Calendar(self.__caldav_client, "%s/%s" % (self.url, calendar))

    def _get_calendar(self, calendar_name):
        """Returns an instance of calendar from a calendar_name

        If the calendar doesn't exist yet, create it
        
        """
        calendar = self.calendars.get(calendar_name, None)
        if calendar is None:
            calendar = self.__make_calendar(calendar_name)
            calendar.save()
            self.calendars[calendar_name] = calendar
        return calendar


    def __init__(self, url, calendars = None):
        self.properties = dict(CalDav.event_properties)
        self.properties.update({"calendar": Property(unicode)})
        super(CalDav, self).__init__(self.properties, ['uid'])
        self.url = url
        self.__caldav_client = DAVClient(url)
        if calendars is None:
            #TODO: fetch calendars from server
            pass
        else:
            self.calendars = dict([(calendar, self.__make_calendar(calendar)) \
                for calendar in calendars])

    def __fetch(self):
        """Returns every events from every known calendar

        """
        for name, calendar in self.calendars.items():
            for event in calendar.events():
                event = event.load()
                itemdict = self.__event_to_item_dict(event)
                item = Item(self, itemdict)
                item.event = event
                item['calendar'] = name
                yield item

    def create(self, properties=None, lazy_loaders=None):
        """Creates a new event

        
            TODO: avoid saving the event on creation, and fetch the uid later
            using the new "auto" api
        """
        caldata = """
BEGIN:VCALENDAR
BEGIN:VEVENT
END:VEVENT
END:VCALENDAR
"""
        properties = properties or {}
        lazy_loaders = lazy_loaders or {} 
        event = Event(self.__caldav_client)
        event.set_data(caldata)
        event.parent = self._get_calendar(properties['calendar'])
        event.save()
        event = event.load()
        remote = self.__event_to_item_dict(event)
        remote.update(properties)
        item = Item(self, remote, lazy_loaders)
        item.event = event
        item.modified = True
        return item

    def search(self, request):
        for item in self.__fetch():
            if request.test(item):
                yield item

    def save(self, item):
        event = item.event
        event.parent = self._get_calendar(item['calendar'])
        for prop in self.properties:
            if item[prop] is not None:
                calprop = event.instance.vevent.contents.get(prop, None)
                if calprop is None:
                    calprop = [event.instance.vevent.add(prop)]
                calprop[0].value = item[prop]
        event.save()

    def delete(self, item):
        item.event.delete()
