# Import necessary modules
from kalamar.access_point.filesystem import FileSystem, FileSystemProperty
from kalamar.site import Site
import os

# Declare a file system access point.
# Items from this access point will be fetched from the root directory
# ~/Music, and will be matched against the pattern
# "artist/album/track - extension
file_ap = FileSystem('/opt/Music/',
        r'(.*)/(.*)/(.*) - (.*)\.(ogg|mp3)',
        ['artist',
         'album',
        #Track is an int, which must be formatted on 2 digits
         ('track', FileSystemProperty(int, formatter="%02d")),
         'title',
         'ext'],
        content_property='stream')

# In order to use this access point, we must register it to a site
kalamar_site = Site()
kalamar_site.register('music', file_ap)
