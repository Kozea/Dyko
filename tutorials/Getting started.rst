Getting Started
===============

:abstract: This tutorial is a quick getting started guide for the Dyko
  framework. Learn how to create a simple blog website from scratch.


.. contents::


Installing Dyko
---------------

See `the documentation page </doc#installation>`_ to install Dyko, with the
SQLAlchemy backend.


Defining a data source (AKA 'access point')
-------------------------------------------

We will begin by defining a simple data model, backed by the sqlite RDBMS.
This data model will consist of only one table, named ``blog_entry``.

The Dyko module responsible for this is the ``kalamar.access_point.alchemy``.

.. note::

   All Kalamar access points are defined in their own submodules within the
   ``kalamar.access_point`` module. The `DykoX project
   <http://gitorious.org/dyko/dykox>`_ provides less stable access points and
   various utilities around Dyko.

To do this, we will need to import the following classes:

.. code-block:: python

   from kalamar.access_point.alchemy import Alchemy, AlchemyProperty
   from kalamar.site import Site

The ``Alchemy`` class is the access point implementation. It is named Alchemy
because it is backed by the `SQLAlchemy SQL toolkit
<http://www.sqlalchemy.org/>`_. The ``AlchemyProperty`` class is responsible
for defining an item property. The ``Site`` class is the main Kalamar entry
point: whenever you want to use an access point, you will have to use the site.

Now that those modules are imported, we can define our blog_entry access point.
It will store entries in an SQLite *entry* table, and have (for now!) only four 
columns:

- ``id``, which will act as an auto generated primary key;
- ``submitted``, the date and time of the post submission;
- ``title``, containing the blog entry title;
- ``content``, containing… well… you guessed it, right?

We'll need to instantiate a Kalamar site, containing an Alchemy access point,
itself containing AlchemyProperties.

Let's begin with the site instantiation:

.. code-block:: python

   site = Site()

That part is rather easy.

Then, we will construct our properties. The following code will create our four
properties:

.. code-block:: python

   title_property = AlchemyProperty(unicode)
   content_property = AlchemyProperty(unicode)
   submitted_property = AlchemyProperty(datetime)
   id_property = AlchemyProperty(int, auto=True)

The first argument to a property definition is always its type. Here, our
properties ``title`` and ``content`` are supposed to hold text, so they are of
the ``unicode`` type.

The third property, ``id``, is slightly different: its type is ``int``, and the
``auto`` keyword argument means that it will be auto-generated for us.

We can now build our access point itself from its properties:

.. code-block:: python

   blog_entry_properties = {
       'id': id_property,
       'title': title_property,
       'content': content_property,
       'submitted': submitted_property}
   blog_entry_access_point = Alchemy(
       'sqlite:///', 'entry', blog_entry_properties, ['id'], createtable=True)

The Alchemy access point constructor is given the following arguments:

- ``'sqlite:///'``: the connection URL to the database. We use here an
  in-memory SQLite database;
- ``'entry'``: the table name;
- A dictionary mapping the property names to their definitions;
- A list containing the name of the properties used as identity properties
  (translated to a primary key definition in the underlying table);
- the ``createtable`` keyword argument, which instructs Kalamar to create the
  underlying table if needed.

And now, we can ``register`` our access point to the Kalamar site:

.. code-block:: python

   site.register('blog_entry', blog_entry_access_point)

We register an access point by passing it to the site along with the name under
which it must be registered.

Let's put the final code in a ``kalamar_site.py`` module:

.. pycode:: tutorials/tutorial2/part1/kalamar_site.py


Filling and querying the database
---------------------------------

Now that your Kalamar is fully setup, let's play with it!

The site offer 4 basic methods for
`CRUD <http://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_
operations:

- create: create an item;
- search: search the access point for matching items;
- delete: delete an item;
- save: save or update an item.

We will begin by creating some items, and saving them to the database:

.. code-block:: python

   first_blog_entry_properties = {
       "title": "My first blog post",
       "content": "Some lightweight content",
       "submitted": datetime(2010, 1, 1)}
   first_blog_entry = site.create("blog_entry", first_blog_entry_properties)
   first_blog_entry.save()

   second_blog_entry_properties = {
       "title": "My second blog post",
        "content": "Some even more lightweight content",
        "submitted": datetime(2010, 3, 22)}
   second_blog_entry = site.create("blog_entry", second_blog_entry_properties)
   second_blog_entry.save()

   third_blog_entry_properties = {
       "title": "Lorem Ipsum",
       "content": "Dolor sic amet",
       "submitted": datetime(2010, 6, 9)}
   third_blog_entry = site.create("blog_entry", third_blog_entry_properties)
   third_blog_entry.save()

   fourth_blog_entry_properties = {
       "id": 3240,
       "title": "Kalamar is Kool",
       "content": "And the gang is too!",
       "submitted": datetime(2010, 8, 1)}
   fourth_blog_entry = site.create("blog_entry", fourth_blog_entry_properties)
   fourth_blog_entry.save()

Now that the items are created and stored in the database, we can query it.

This first example uses the ``search`` method, without any query. It will list
every single entry from the database, and dump it to the console:

.. code-block:: python

   for item in site.search("blog_entry"):
       print "Post ID #%s: %s" % (item["id"], item["title"])
       print item["content"]

.. pyexec:: tutorials/tutorial2/part2/search_simple.py

Another example, this time using a simple query:

.. code-block:: python

   for item in site.search("blog_entry", {"title": "Kalamar is Kool"}):
       print "Post ID #%s: %s" % (item["id"], item["title"])
       print item["content"]

.. pyexec:: tutorials/tutorial2/part2/search_query2.py

The dictionary notation for a request is just a shortcut for its object
counterpart: the ``kalamar.request`` module offers what you need to perform
more advanced queries. Here are some examples:

.. pycode:: tutorials/tutorial2/part2/search_query3.py

.. pyexec:: tutorials/tutorial2/part2/search_query3.py


And now for something completely different… Kraken!
---------------------------------------------------

Kraken is the web part of Dyko. It's a minimalistic web framework designed
towards really simple applications.

We will setup the basic layout for our site. The default configuration expects
the following directory structure::

    ./myproject
        /views
            some templates

In the ``views`` directory, you can put files that you want Kraken to serve as
templates. Templates are matched by URLs, mime-type and template engine.

For example, the following files in the views directory would be served as
follow:

``index.html.jinja2``
  On ``/``, with mime-type html, using the Jinja2 template engine.

``style.css.genshi``
  On ``/style``, with mime-type css, using the Genshi template engine.

``dblist.html.jinja2``
  On ``/dblist``, with mime-type html, using the Jinja2 template engine.

To use a Kraken instance, just use the following code:

.. code-block:: python

   import kraken.site

   site = kraken.site.Site()
   kraken.runserver(site)

Copy this code in the ``myproject/kraken_site.py`` file, and run the server::

    python kraken_site.py

This will start the server on localhost, port 5000.

Now, you just have to fill it with some content. Add a file named
``hello_world.html.jinja2`` in the views directory, containing a basic Jinja2
hello world.

.. pycode:: tutorials/tutorial2/part3/views/hello_world.html.jinja2 jinja

.. note::

   The double-brackets is a print statement in the Jinja2 template engine.  It
   evaluates whatever statement between the brackets, and prints its result.

Now, open your browser to `<http://localhost:5000/hello_world/>`_, you should
see the following result:

.. werkzeugurl:: tutorials/tutorial2/part3/test_url.py /hello_world/

Because Kraken is designed to be used with Kalamar, you can initiate the Kraken
site with a Kalamar site. Copy your former Kalamar site to a ``blog_kalamar``
module.

.. pycode:: tutorials/tutorial2/part3/blog_kalamar.py

And update ``kraken_site.py`` with the following:

.. pycode:: tutorials/tutorial2/part3/kraken_site.py

You should now have the following directory structure::

    myproject
        /kraken_site.py
        /blog_kalamar.py
        /views
            /hello_world.html.jinja2

You can now use your Kalamar site from within your application.
Open a new ``views/index.html.jinja2`` file, and create a simple template:

.. pycode:: tutorials/tutorial2/part3/views/index.html.jinja2 jinja

.. werkzeugurl:: tutorials/tutorial2/part3/test_url.py /

Those hard-coded blog-posts look kinda ugly. Maybe we should add a form to add
posts?


Using Controllers
-----------------

Kraken offer some basic solutions to implement code that doesn't belong to in the
template.

Two python decorators are available for this:

- ``expose``: this decorator expose a function to the specified url. The function
  must return a valid ``Response`` object.
- ``expose_template``: this decorator behaves exactly like ``expose``, except
  that the decorated function is not supposed to return a response, but rather
  a dictionary used as data in the corresponding template.

Before managing a full form, let's implement a simple page for viewing one
comment at a time.

Create a new module, ``controllers.py``, containing the following code:

.. code-block:: python

   from kraken.site import expose_template
   import  blog_kalamar

   @expose_template('/post/<int:post_id>')
   def blog_post(request, post_id, **kwargs):
       post = blog_kalamar.site.open('blog_entry', {'id': post_id})
       return {'blog_entry': post}

The ``controllers`` module be registered in the site, with the
``register_controllers`` method:

.. pycode:: tutorials/tutorial2/part4/kraken_site.py

The ``@expose_template`` decorator makes this URL available from
``/post/<any_post_id>``. With the default configuration, the values it returns
will be injected in a template whose name (without the extension, nor template
extension) is ``post``.

So, let's create the post/index.html.jinja2 template!

.. pycode:: tutorials/tutorial2/part4/views/post/index.html.jinja2 jinja

Now, let's tweak the index page to include permalinks to the individual posts:

.. pycode:: tutorials/tutorial2/part4/views/index.html.jinja2 jinja

Following one of those links should yield the following results:

.. werkzeugurl:: tutorials/tutorial2/part4/test_url.py /post/3240

Armed with this new knowledge, we can procede on adding more controllers to add
a blog post!

First, we can create the page containing the form used for adding a post:

.. pycode:: tutorials/tutorial2/part4/views/post/add.html.jinja2 html

Now, we will need a to process the form submission. For this, we will register
a controller for the same /post/add url, but specialized for the POST method:

.. pycode:: tutorials/tutorial2/part4/controllers.py

We use the ``expose`` decorator instead of ``expose_template``, because we want
to redirect the user in order to avoid resubmission (using the `"303" HTTP
status code <http://en.wikipedia.org/wiki/HTTP_303>`_).

And now, we can add our own blog posts!

That's interesting, but what is a blog post without any comments? And here comes in…


Kalamar relations
-----------------

We will now attach comments to our blog post.

To do this, we will have to modify our model: we will add a "comments" access
point, as well as two relationships from the comments to the blog entry, and
from the blog entry to their attached comments.

Let's see the comments property definition for the blog_entry access point:

.. code-block:: python

   comments_property = AlchemyProperty(iter,
       relation='one-to-many',
       remote_ap='comment',
       remote_property='blog_entry')

It's type is iter, because a blog entry is associated to multiple comments.
This is also why we have to specify that the relationship is a 'one-to-many'
relationship.  The ``remote_ap`` argument refers to the name under which the
other access point is registered, and ``remote_property`` is used to retrieve
the comments linked to this entry.

Similarly, this is how we define the comments access point:

.. code-block:: python

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

So the whole source code for the Kalamar site reads like this:

.. pycode:: tutorials/tutorial2/part5/blog_kalamar.py

This relationship exists, but it's not used yet. We should create a
``/post/comments/add`` URL for posting a new comment, and a list of all
comments below each post:

.. pycode:: tutorials/tutorial2/part5/views/post/index.html.jinja2 jinja

And the associated controller:

.. code-block:: python
    
   @expose("/post/<int:post_id>/comment", methods=("POST",))
   def add_blog_comment(request, post_id):
       content = request.values["comment_input"]
       post = blog_kalamar.site.open("blog_entry", {"id": post_id})
       submitted = datetime.now()
       new_comment_properties = {
           "content": content,
           "submitted": submitted,
           "blog_entry": post}
       new_comment = blog_kalamar.site.create("comment", new_comment_properties)
       new_comment.save()
       return redirect(request, "/post/%s" % post_id, status=303)


The ``view`` method
-------------------

The view method provides additional capabilities to query a Kalamar access
point.

Using the ``view`` queries, you can:

- Return partial view of an item;
- Return attributes from different items linked together by a relationship;
- Filter on attributes from different items;
- Order your queries;
- Return only a specific range (for example, the first 10 items).

We'll use the view method to display only the 10 latest post on the index page:

.. pycode:: tutorials/tutorial2/part5/views/index.html.jinja2 jinja

The ``order_by`` argument must be a list of tuples.

.. code-block:: python

   order_by = [('submitted', False)]

That means that we order the entries by the 'submitted' attribute, in
descending order (the ``False`` value).

The ``select_range`` argument can be either an integer or a tuple. An integer
value limits the results, whereas a tuple argument represents a range.

.. code-block:: python

   # Select the first 10 items
   select_range = 10
   # It is equivalent to:
   select_range = (0,10)

Let's take a look at some example queries, using our blog site.  Select all
comments attached to blog posts published before 2000.

.. code-block:: python

   condition = Condition('blog_entry.submitted', '<', datetime(2000,1, 1))
   kalamar.view('comment', request=condition)

Select only the date from previous comments, along with the entry date:

.. code-block:: python

   aliases = {
       'comment_date': 'submitted',
       'entry_date': 'blog_entry.submitted'}
   kalamar.view('comment', request=condition, aliases=aliases)

Select distinct comment content:

.. code-block:: python

   kalamar.view('comment', aliases={'content': 'content'}, distinct=True)




