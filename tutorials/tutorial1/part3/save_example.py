# Import the previously defined module
from kalamar_site import kalamar_site
from utils import dump_item

# New item creation
new_file_properties = {
    "artist": "The Phase",
    "album": "Dogma",
    "track": 2,
    "title": "Dirty Angel",
    "duration": 3500,
    "copyright": "CC-BY-NC-SA"}
new_file_item = kalamar_site.create("music", new_file_properties)

# Let"s save it!
new_file_item.save()

# And now, query the database...
for item in kalamar_site.search("music"):
    dump_item(item)
