#import the previously defined module
from kalamar_site import kalamar_site
from kalamar.access_point import NotOneMatchingItem
import os.path


#The open method works like search, except it return one and only one item.
#It the given criteria matches more or less than one item, it throws an exception
try:
    kalamar_site.open('music', {'track': 2})
except NotOneMatchingItem:
    print "Oups, seems like our query is not what we meant"


#Fetching the item we want to delete
item_to_delete = kalamar_site.open('music', {'title': 'Dirty Angel',
    'album': 'Dogma'})

#Deleting the item
item_to_delete.delete()


