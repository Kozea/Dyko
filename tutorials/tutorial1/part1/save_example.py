#import the previously defined module
from kalamar_site import kalamar_site
import os.path

#This is the file we want to add to our collection
music_file = open(os.path.expanduser(os.path.join('~','Music','Dirty angel.mp3')))

#New item creation
new_file_item = kalamar_site.create('music', {
    'artist': 'The Phase',
    'album': 'Dogma',
    'track': 2,
    'title': 'Dirty Angel',
    'ext': 'ogg',
    'stream': music_file})

#Let's save it!
new_file_item.save()
