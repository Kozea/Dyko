from mutagen_ap import MutagenAP, MutagenProperty
from kalamar.access_point.filesystem import FileSystem, FileSystemProperty
import os

file_ap = FileSystem(os.path.expanduser('~/Music/'),
        r'(.*)/(.*)/(.*) - (.*)\.(ogg|mp3)',
        ['artist',
         'album',
        #Track is an int, which must be formatted on 2 digits
         ('track', FileSystemProperty(int, formatter="%02d")),
         'title',
         'ext'],
        content_property='stream')

mutagen_ap = MutagenAP(file_ap, {
    'artist': MutagenProperty(unicode, 'Artist'),
    'album' : MutagenProperty(unicode, 'Album'),
    'duration': MutagenProperty(int, 'length'),
    'copyright': MutagenProperty(unicode, 'copyright')
    },
    'stream')

