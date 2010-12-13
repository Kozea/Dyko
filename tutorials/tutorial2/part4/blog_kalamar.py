from kalamar.access_point.alchemy import Alchemy, AlchemyProperty
from kalamar.site import Site
from datetime import datetime

site = Site()

title_property = AlchemyProperty(unicode)
content_property = AlchemyProperty(unicode)
submitted_property = AlchemyProperty(datetime)
id_property = AlchemyProperty(int, auto=True)


blog_entry_access_point = Alchemy("sqlite:///", "entry", {
    'id' : id_property,
    'title': title_property,
    'content': content_property,
    'submitted': submitted_property},
    ['id'],
    createtable = True)

site.register('blog_entry', blog_entry_access_point)

first_blog_entry = site.create('blog_entry', {
    'title': 'My first blog post',
    'content': 'Some lightweight content',
    'submitted': datetime(2010, 1, 1)
})
first_blog_entry.save()

second_blog_entry = site.create('blog_entry', {
    'title': 'My second blog post',
    'content': 'Some even more lightweight content',
    'submitted': datetime(2010, 3, 22),
})
second_blog_entry.save()

third_blog_entry = site.create('blog_entry', {
    'title': 'Lorem Ipsum',
    'content': 'Dolor sic amet',
    'submitted': datetime(2010, 6, 9),
})
third_blog_entry.save()

fourth_blog_entry = site.create('blog_entry', {
    'id': 3240,
    'title': 'Kalamar is Kool',
    'content': 'And the gang is too!',
    'submitted': datetime(2010, 8, 1),
})
fourth_blog_entry.save()
