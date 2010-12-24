# Import the previously defined module
from kalamar_site import kalamar_site
import os.path

# This is the file we want to add to our collection
music_file = open(os.path.join("opt", "Music", "Dirty angel.mp3"))

# New item creation
new_item_properties = {
    "artist": "The Phase",
    "album": "Dogma",
    "track": 2,
    "title": "Dirty Angel",
    "ext": "ogg",
    "stream": music_file}
new_file_item = kalamar_site.create("music", new_item_properties)

# Let's save it!
new_file_item.save()
