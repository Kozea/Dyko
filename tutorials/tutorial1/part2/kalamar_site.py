from mutagen_ap import MutagenAP, MutagenProperty
from kalamar.access_point.filesystem import FileSystem, FileSystemProperty
from kalamar.site import Site

# Declare a file system access point.
# Items from this access point will be fetched from the root directory
# /opt/Music, and will be matched against the pattern
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

#Now, we have to wrap the previous access point in our new mutagen access point
mutagen_ap = MutagenAP(file_ap, {
    'artist': MutagenProperty(unicode, 'Artist'),
    'album' : MutagenProperty(unicode, 'Album'),
    'duration': MutagenProperty(int, 'length'),
    'copyright': MutagenProperty(unicode, 'copyright')
    },
    'stream')

kalamar_site = Site()
kalamar_site.register('music', mutagen_ap)
