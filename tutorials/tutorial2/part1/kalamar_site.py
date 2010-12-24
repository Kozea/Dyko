from datetime import datetime
from kalamar.access_point.alchemy import Alchemy, AlchemyProperty
from kalamar.site import Site


site = Site()

blog_entry_properties = {
    "id": AlchemyProperty(int, auto=True),
    "title": AlchemyProperty(unicode),
    "submitted": AlchemyProperty(datetime),
    "content": AlchemyProperty(unicode)}
blog_entry_access_point = Alchemy(
    "sqlite:///", "entry", blog_entry_properties, ["id"], createtable=True)

site.register("blog_entry", blog_entry_access_point)
