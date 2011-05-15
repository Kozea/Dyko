Simple Application using Kalamar
================================

:abstract: Create a simple music database with a command-line interface.

.. contents::

Goal
----

This tutorial's goal is to introduce the reader to the Kalamar data access
layer.

The only prerequisites for the first part are:

- having `Dyko installed </doc#installation>`_;
- knowing a little bit of Python.

In following parts, additional dependencies will be required (like `SQLAlchemy
<http://www.sqlalchemy.org/>`_ or `Mutagen
<http://code.google.com/p/mutagen/>`_).

After a succinct description of Kalamar core concepts, we will use Kalamar to 
perform search on a music collection using a command-line interface.

Then, we will implement our own access point to extract Vorbis comments (tags)
from our music collection.

In a third part, we will populate a database with those tags, and show how
powerful Kalamar relationships are to link heterogenous data sources.


Concepts
--------

Kalamar is structured around a handful of concepts.

Access Point
************

An access point is a data access layer allowing simple `CRUD
<http://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_ operations on
a datasource.

Currently, Kalamar is shipped with the following implementations:

- an access point to save data into files;
- an access point backed up by an RDBMS (using SQLAlchemy);
- an access point storing data in memory.

An access point instance is associated with a set of properties definition,
defining the properties and their types that each item will provide.

In this tutorial, we will define our first access point as a mean to access
file-system based music files.
    
Site
****

The Kalamar Site is the central object. Access points are registered against
the site, which is used to query the access points.

Access Point Wrappers
*********************

An access point wrapper offer the same API as an access point, but sits on top
of another access point rather than accessing data directly. In this tutorial,
we will implement an access point wrapper for extracting ID tags information
from music files.


Tutorial
--------

Querying a file system
**********************

Let's assume we have a music collection on our hard-drive, located at
``/opt/Music``, structured like this::

  /opt/Music
      /Artist1
          /Album1
              /title1.ogg
              /title2.ogg
              /title3.ogg
          /Album2
              /title1.ogg
              /title2.ogg
      /Artist2
          /Album1
              /title1.ogg
              /title2.ogg
              /title3.ogg
              /title4.ogg

We want to be able to search those items by artist, album or title.

You can freely download the `sample music collection </data/music.tar.gz>`_.

The sample music collection only contains CC-licensed titles, downloaded from
Jamendo.

In a file named ``kalamar_site.py``, copy the following code:

.. pycode:: projects/dyko/tutorials/tutorial1/part1/kalamar_site.py

We can then perform some simple search on it, using the following code.

The site ``search`` method takes an access point name (``'music'``, in our
case) and an (optional) query.

Let's define a small ``utils`` module, containing basic display code:

.. pycode:: projects/dyko/tutorials/tutorial1/part1/utils.py

Now, we can dump the whole database by performing a search on the ``'music'``
access point, without any query. Here is the code:

.. pycode:: projects/dyko/tutorials/tutorial1/part1/search_example.py

Which, once executed, gives the following output:

.. pyexec:: projects/dyko/tutorials/tutorial1/part1/search_example.py

You can pass a query to the search method. The query must be either a
``Request`` instance, or a dictionary for syntactic sugar.

.. pycode:: projects/dyko/tutorials/tutorial1/part1/search_query_example.py

Yields the following results:

.. pyexec:: projects/dyko/tutorials/tutorial1/part1/search_query_example.py

Now, let's say we want to add a music file to our collection:

.. pycode:: projects/dyko/tutorials/tutorial1/part1/save_example.py

If you visit the ``/opt/Music`` directory, you will notice that the directory
structure corresponding to the artist, album, etc. has been created for you.

Similarly, you can now delete the same file from your collection:

.. pycode:: projects/dyko/tutorials/tutorial1/part1/delete_example.py

Once executed, this code deletes your item and the empty directories left
behind it.

Implementing an AccessPointWrapper: parsing Vorbis comments
***********************************************************

Now that our collection is structured on the file system, several limitations
arise.

On any access points, a set of properties are defined as 'identity
properties'. Identity properties are similar to primary keys in RDBMS.
Those identity properties cannot be modified. On a file system access
point, every property is an identity property, except for the content
property.

Moreover, we may want to add additional information on the file.

In Ogg Vorbis audio files, Vorbis comments are a great way to store such
information.

We will use the AcessPointWrapper faciity to parse and write Vorbis comments
with the `Mutagen library <http://code.google.com/p/mutagen/>`_

Kalamar ships with a ``Decorator`` access point designed specifically for
that. The decorator access point add a few properties to an access point
definition which are computed from other properties. This is especially useful
if you need to use Kalamar to read and write structured files.

So, here is the source code. That's quite long, but the comments will guide you
through the whole process.

.. note::

   Subclassing the ``DecoratorItem`` in the following code is not required, and
   has been done only to avoid reparsing the whole file each time a property
   from the tags is accessed

.. pycode:: projects/dyko/tutorials/tutorial1/part2/mutagen_ap.py

We can now use this access point instead of the previous one.

.. pycode:: projects/dyko/tutorials/tutorial1/part2/kalamar_site.py

In order to show our changes, we just have to change the dump_item method we
used to display items:

.. pycode:: projects/dyko/tutorials/tutorial1/part2/utils.py

And the exact same code can be run again on the access point, now displaying the
added properties:

.. pyexec:: projects/dyko/tutorials/tutorial1/part2/search_query_example.py

The update example shows how to set tags on the defined tags on the file.

.. pycode:: projects/dyko/tutorials/tutorial1/part2/update_example.py

And when running the search example again, you can confirm the tag has actually
been update:

.. pyexec:: projects/dyko/tutorials/tutorial1/part2/search_example.py

Moving to a database
********************

So far we have provided a way to query against a file system, but as our music
collection grows, the query performance will have to be better than parsing
everything on the file system.

Let's say we want to store the metadata in a database, and the actual files on a
filesystem.

Let's begin with the database part.

The alchemy access point allows us to use SQLAlchemy to access any RDBMS.

.. pycode:: projects/dyko/tutorials/tutorial1/part3/kalamar_site.py

Then, populating and querying the database is as easy as previously (after some
tweaking to our dump_item method, removing the 'ext' property):

.. pycode:: projects/dyko/tutorials/tutorial1/part3/save_example.py

.. pyexec:: projects/dyko/tutorials/tutorial1/part3/save_example.py

So we can preserve the same API, while changing the concrete storage
implementation. Let's fill our SQLite database with the access point created
previously!

.. pycode:: projects/dyko/tutorials/tutorial1/part3/data_migration.py

.. pyexec:: projects/dyko/tutorials/tutorial1/part3/data_migration.py

Obviously, we should store these data elsewhere than in an in-memory database.
But for the sake of this tutorial, let's keep it like this.

This leads us to the next section...

Exploring Kalamar relationships
*******************************

Now that our tags are in the database, it would be nice to access the files
directly from the database item.

Our data model will consist of:

- a track metadata, stored in the database,
- linked with a file on the file system.

For this implementation, we will slightly change our model to take this
relationship into account:

.. pycode:: projects/dyko/tutorials/tutorial1/part4/kalamar_site.py

Migrating our data is as easy as before, we just have to add the old item as a
property.

.. pycode:: projects/dyko/tutorials/tutorial1/part4/data_migration.py

.. pyexec:: projects/dyko/tutorials/tutorial1/part4/data_migration.py

And using our good old search code, modified for the occasion, we can access the
file on the file system directly from the item returned from the database.

.. pycode:: projects/dyko/tutorials/tutorial1/part4/search_example.py

.. pyexec:: projects/dyko/tutorials/tutorial1/part4/search_example.py

