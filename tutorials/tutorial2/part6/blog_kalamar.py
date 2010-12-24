from datetime import datetime

from kalamar.access_point.alchemy import Alchemy, AlchemyProperty
from kalamar.site import Site
from kalamar.item import Item


site = Site()

title_property = AlchemyProperty(unicode)
content_property = AlchemyProperty(unicode)
submitted_property = AlchemyProperty(datetime)
id_property = AlchemyProperty(int, auto=True)
comments_property = AlchemyProperty(
    iter, relation="one-to-many",
    remote_ap="comment", remote_property="blog_entry")

blog_entry_properties = {
    "id": id_property,
    "title": title_property,
    "content": content_property,
    "submitted": submitted_property,
    "comments": comments_property}
blog_entry_access_point = Alchemy(
    "sqlite:///", "entry", blog_entry_properties, ["id"], createtable=True)

blog_entry_property = AlchemyProperty(
    Item, relation="many-to-one",
    remote_ap="blog_entry", remote_property="id")

comments_properties = {
    "id": AlchemyProperty(int, auto=True),
    "content": AlchemyProperty(unicode),
    "submitted": AlchemyProperty(datetime),
    "blog_entry": blog_entry_property}
comments_access_point = Alchemy(
    "sqlite:///", "comments", comments_properties, ["id"], createtable=True)

site.register("blog_entry", blog_entry_access_point)
site.register("comment", comments_access_point)
