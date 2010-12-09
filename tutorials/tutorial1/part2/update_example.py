#import the previously defined module
from kalamar_site import kalamar_site
from kalamar.access_point import NotOneMatchingItem
import os.path

#Fetching the item we want to update
item_to_update = kalamar_site.open('music', {'title': 'Balrog Boogie'})

item_to_update['album'] = 'ANOTHER UNKNOWN ALBUM'

#Updating the item
item_to_update.save()
