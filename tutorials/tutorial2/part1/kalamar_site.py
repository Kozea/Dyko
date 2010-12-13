from kalamar.access_point.alchemy import Alchemy, AlchemyProperty
from kalamar.site import Site
from datetime import datetime

site = Site()

blog_entry_access_point = Alchemy("sqlite:///", "entry", {
    'id' : AlchemyProperty(int, auto=True),
    'title': AlchemyProperty(unicode),
    'submitted': AlchemyProperty(datetime),
    'content': AlchemyProperty(unicode)},
    ['id'],
    createtable = True)

site.register('blog_entry', blog_entry_access_point)
