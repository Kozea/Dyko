# Import necessary modules
from kalamar.access_point.alchemy import Alchemy, AlchemyProperty
from kalamar.site import Site


# Database URL. If you want to use a different database, please refer
# to the qlalchemy documentation regarding url schemes
URL = 'sqlite://'

# Declare a database access point, with the connect string, the table
# name and the mapped properties
db_ap = Alchemy(URL, 'music',
        {'artist':  AlchemyProperty(unicode),
         'album': AlchemyProperty(unicode),
         'track': AlchemyProperty(int),
         'title': AlchemyProperty(unicode),
         'duration': AlchemyProperty(int),
         'copyright': AlchemyProperty(unicode),
         'id' : AlchemyProperty(int, auto=True)
         },
        # Contrary to the file system access point, the alchemy access
        # point must be told what are its identity properties. Here, we
        # choose a silent key
        ['id'],
        createtable=True)

# In order to use this access point, we must register it to a site
kalamar_site = Site()
kalamar_site.register('music', db_ap)


# We import the good old mutagen access point from part2,
# because we will use it to populate or database
from part2_ap import mutagen_ap

kalamar_site.register('old_music', mutagen_ap)
