
Dyko - Kalamar
**************

Kalamar is an object-relational mapping library for the Python
language. Its concept is based on our called "access-point".


Site
====

class class kalamar.Site(config_filename=None, fail_on_inexistent_parser=True)

   Kalamar site.

   exception exception FileNotFoundError

      File not found on filesystem.

   exception exception Site.MultipleObjectsReturned

      More than one object have been returned.

   exception exception Site.NotOneObjectReturned

      Not one object has been returned.

   exception exception Site.ObjectDoesNotExist

      No object has been returned.

   Site.create_item(access_point_name, properties)

      Return an item.

      TODO document & test

   Site.generate_primary_values(access_point_name)

      Return dict of primary keys and values for
      ``access_point_name``.

   Site.get_description(access_point_name)

      Return a tuple of strings or None.

      Return the keys defined in configuration or None if
      ``access_point_name`` does not exist.

   Site.isearch(access_point, request=None)

      Return a generator of items in ``access_point`` matching
      ``request``.

      See ``Site.parse_request`` for the syntax of the ``request``
      string.

   Site.item_from_filename(filename)

      Search all access points for an item matching ``filename``.

      Return the first item found or None.

   Site.open(access_point, request=None)

      Return the item in access_point matching request.

      If there is no result, raise ``Site.ObjectDoesNotExist``. If
      there are more than 1 result, raise
      ``Site.MultipleObjectsReturned``.

   static Site.parse_request(request)

      Convert a ``request`` to a list of Condition objects.

      If ``request`` is a string, parse it with our query language. If
      it’s a number, parse its string representation. If it’s a dict,
      assume equality for all operators. Otherwise, assume it’s a list
      of values

      >>> Site.parse_request(u"/'1'/b='42'/c>='3'/")
      ...                                  # doctest: +NORMALIZE_WHITESPACE
      [Condition(None, None, u'1'),
       Condition(u'b', <built-in function eq>, u'42'),
       Condition(u'c', <built-in function ge>, u'3')]

      >>> Site.parse_request({u'a': 1, u'b': None})
      ...                                  # doctest: +NORMALIZE_WHITESPACE
      [Condition(u'a', None, 1),
       Condition(u'b', None, None)]

      >>> Site.parse_request(1)            # doctest: +NORMALIZE_WHITESPACE
      [Condition(None, None, 1)]

   static Site.remove(item)

      Remove/delete the item from the backend storage.

   Site.remove_many(access_point, request)

      Remove all items matching the request

   static Site.save(item)

      Update or add the item.

   Site.search(access_point, request=None)

      List all items in ``access_point`` matching ``request``.

      See ``Site.parse_request`` for the syntax of the ``request``
      string.


Item
====

Base classes to create kalamar items.

Parsers must: - inherit from Item - have a ``format`` class attribute
as a string, - extend or override the _parse_data method, - override
the serialize method.

The ``format`` string is used to identify the parser in configuration
files and must be unique.

See BinaryItem for a very simple example.


Class Item
----------

class class kalamar.item.Item(access_point, opener=None, storage_properties={})

   Base class for parsers.

   Items dictionnary-like: you can use the item['…'] syntax to get and
   set properties. Missing properties default to None.

   The _access_point attribute represents where, in kalamar, the item
   is stored. It is an instance of AccessPoint.

   Items are hashable but mutable, use hash with caution.

   access_point_name

      Return a request sufficient to find this item and only this one.

   static create_item(access_point, properties=None, initial_content=None)

      Return a new item instance.

      Parameters: - ``access_point``: instance of the access point
      where the item

         will be reachable (after saving).

      * ``properties``: dictionnary or MultiDict of the item
        properties. These properties must be coherent with what is
        defined for the access point.

      * ``initial_content``: some initial content for parsers needing
        it.

      Fixture >>> from _test.corks import CorkAccessPoint >>> ap =
      CorkAccessPoint() >>> properties = {}

      Test >>> item = Item.create_item(ap, properties) >>> assert
      item.format == ap.parser_name >>> assert isinstance(item, Item)

   encoding

      Return the item encoding.

      Return the item encoding, based on what the parser can know from
      the item data or, if unable to do so, on what is specified in
      the access_point.

   filename

      Return the file path.

      If the item is stored in a file, return its path/name. Else
      return None.

   keys()

      Return the name of all properties.

   modified

      Return if the item has been modified since creation.

      The item is considered changed if any storage or parser property
      has been changed since its creation.

   parser_properties

      The “parser” counterpart of storage_properties.

      This is also a cached_property because we need the actual
      raw_parser_properties MultiDict to instanciate it.

   raw_parser_properties

      The “parser” counterpart of raw_storage_properties. A MultiDict.

      Parser properties are lazy: only parse when needed.

   request

      Return a request sufficient to find this item and only this one.

      This ``request`` must be canonical. As a consequence, opening an
      item twice should give the same ``request``, even if the request
      used for opening the items are not the same.

      This property is used for testing item equality.

   serialize()

      Return raw content as bytestring.

   test_condition(condition)

      Return True if item properties matches this condition.


Parser
======


Class TextItem
--------------

class class kalamar.parser.textitem.TextItem(access_point, opener=None, storage_properties={})

   Access item data as a unicode string.


Class RestAtom
--------------

class class kalamar.parser.rest.RestAtom(access_point, opener=None, storage_properties={})

   This parser simply exposes ReST metadata as properties.

   These properties are read-only: your modifications will *not* be
   saved if you change them.


Class RestCapsule
-----------------

class class kalamar.parser.rest.RestCapsule(access_point, opener=None, storage_properties={})

   A ReStructuredText capsule.

   The ReST document is only made of metadata and :include:
   directives. Any other content (such as text) is discarded and will
   be lost when the capsule is saved.

   Metadata are exposed as properties, and :include:’s as subitems.
   The filenames are resolved to the actual kalamar items, or a
   MissingItem if no item matched the filename.


Class MessageItem
-----------------

class class kalamar.parser.mail.MessageItem(access_point, opener=None, storage_properties={})

   Parse email messages using python builtin email module.


Class OneToManyDBCapsule
------------------------

class class kalamar.parser.db_capsule.OneToManyDBCapsule(access_point, opener=None, storage_properties={})

   TODO doc


Class ManyToManyDBCapsule
-------------------------

class class kalamar.parser.db_capsule.ManyToManyDBCapsule(access_point, opener=None, storage_properties={})

   A capsule format for items stored in databases.

   This parser can store capsules in databases without additional
   public access points.

   A table is needed in the same database as the capsule (but not
   necessarily in the same database as the subitems). This table is
   called the linking table, as it links the capsule access point and
   the item access point.


Class GenericManyToManyDBCapsule
--------------------------------

class class kalamar.parser.db_capsule.GenericManyToManyDBCapsule(access_point, opener=None, storage_properties={})

   A capsule format for items stored in databases.

   This parser can store capsules in databases without additional
   public access points.

   A table is needed in the same database as the capsule (but not
   necessarily in the same database as the subitems). This table is
   called the linking table, as it links the capsule access point and
   the item access point.


Storage
=======


Class AccessPoint
-----------------

Default access point.

``AccessPoint`` is the class to override in order to create storage
access points.

class class kalamar.storage.base.AccessPoint(**config)

   Abstract class for all storage backends.

   Attributes:

   * config: a dictionnary of the access point configuration.

   * default_encoding: default character encoding used if the parser
     does not have one. Read-only attribute.

   * property_names: properties defined in the access_point
     configuration.

   * url: where the data is available.

   * basedir: directory from where relatives pathes should start.

   expand_syntaxic_sugar(conditions)

      Expand syntaxic sugar in requests.

      ``conditions`` is a list of (property_name, operator, value)
      tuples as returned by kalamar.site.Site.parse_request.

      If ``operator`` is None, set it to ``kalamar.utils.equals``.

      If ``property_name`` is None in the n-th condition, set it to
      the n-th property of this access point.

      >>> ap = AccessPoint(url='', storage_aliases='a=p1/b=p2/c=p3')
      >>> list(ap.expand_syntaxic_sugar([
      ...     utils.Condition(None, None,              1),
      ...     utils.Condition(None, utils.operator.gt, 2),
      ...     utils.Condition('c', None,               3),
      ...     utils.Condition('d', utils.operator.ge,  4)
      ... ])) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
      [Condition('a', <built-in function eq>, 1),
       Condition('b', <built-in function gt>, 2),
       Condition('c', <built-in function eq>, 3),
       Condition('d', <built-in function ge>, 4)]

   classmethod from_url(**config)

      Return an instance of the appropriate class according to the
      URL.

      >>> AccessPoint.from_url(url='nonexistent-protocol://…')
      Traceback (most recent call last):
          ...
      ValueError: Unknown protocol: nonexistent-protocol

   generate_primary_values()

      Generate a dict with primary keys and unused values.

      This function is particularly useful to create new items on a
      storage unable to automatically generate meaningless primary
      keys (such as filesystems, or databases without sequences).

      This property has to be overriden.

   get_storage_properties()

      Return the list of properties used by the storage (not aliased).

      This method has to be overriden.

   item_from_filename(filename)

      Search for an item matching this filename.

      Storage that do not store items in files should leave this
      implementation that return the NotImplemented constant.

      Else, this method has to be overriden.

   primary_keys

      List of primary keys names.

      Here, "primary key" must be understood as "a sufficient set of
      keys to make a request returning 0 or 1 object".

      This list must be ordered and stable for a given access point,
      in order to construct canonical requests for items.

      This property has to be overriden.

   remove(item)

      Remove/delete the item from the backend storage.

      This method has to be overriden.

   remove_many(conditions)

      Remove all items matching the request.

   save(item)

      Update or add the item.

      This method has to be overriden.

   search(conditions)

      Generate a sequence of every item matching "conditions".

      "conditions" is a list of utils.Condition objects as returned by
      kalamar.site.Site.parse_request.


Class DBAPIStorage
------------------

Database access point.

DBAPIStorage is just a base class to construct different databases
access points.

class class kalamar.storage.dbapi.DBAPIStorage(*args, **kwargs)

   Base class for SQL SGBD Storage.

   Descendant class must override ``get_connection``,
   ``primary_keys``, ``get_db_module`` and ``protocol``.

   It may be useful to also redefine the following methods or
   attributes:

   * ``_quote_name``

   * ``_sql_escape_quotes``

   * ``sql_operators``


Class FileSystemStorage
-----------------------

Filesystem access point.

This implementation relies on default python filesystem functions and
should work on all platforms.

class class kalamar.storage.filesystem.FileSystemStorage(**config)

   Store items in files.


Class MySQLdbStorage
--------------------

MySQL access point.

This implementation depends on DBAPIStorage, the generic SQL database
access point.


Class PostgreSQLStorage
-----------------------

PostgreSQL access point.

This implementation depends on DBAPIStorage, the generic SQL database
access point.


Class SQLiteStorage
-------------------

SQLite 3 access point.

This implementation depends on DBAPIStorage, the generic SQL database
access point.

class class kalamar.storage.sqlite.SQLiteStorage(*args, **kwargs)

   SQLite 3 access point


Utils
=====

Kalamar various utils.

kalamar.utils.apply_to_result(function)

   Make a decorator that applies ``function`` to the results.

   >>> @apply_to_result(list)
   ... def foo():
   ...     "A generator"
   ...     yield 'bar'
   >>> foo.__doc__
   'A generator'
   >>> foo()
   ['bar']

kalamar.utils.re_match(string, pattern)

   Return if ``string`` matches ``pattern``.

kalamar.utils.re_not_match(string, pattern)

   Return if ``string" does not match ``pattern``.

kalamar.utils.recursive_subclasses(class_)

   Return all ``class_`` subclasses recursively.

kalamar.utils.simple_cache(function)

   Decorator that caches function results.

   The key used is a hash of the ``repr()`` of all arguments. The
   cache dict is accessible as the ``cache`` attribute of the
   decorated function.

   Warning: the results stay in memory until the decorated function is
   garbage-collected or you explicitly remove them.

   TODO: Maybe automatially remove results that weren’t used for a
   long time?

   >>> @simple_cache
   ... def f():
   ...     print 'Computing the answer...'
   ...     return 42
   >>> f()
   Computing the answer...
   42
   >>> f()
   42
   >>> f.cache # doctest: +ELLIPSIS
   {'...': 42}
   >>> f.cache.clear()
   >>> f.cache
   {}


Class OperatorNotAvailable
--------------------------

class class kalamar.utils.OperatorNotAvailable

   Operator unavailable in operators.


Class ParserNotAvailable
------------------------

class class kalamar.utils.ParserNotAvailable

   Parser unavailable in parsers.


Class Condition
---------------

class class kalamar.utils.Condition(property_name, condition_operator, value)

   A contener for property_name, condition_operator, value.


Class ModificationTrackingList
------------------------------

class class kalamar.utils.ModificationTrackingList(*args, **kwargs)

   List with a ``modified`` attribute becoming True when the list
   changes.

   >>> l = ModificationTrackingList(range(3))
   >>> l
   ModificationTrackingList([0, 1, 2])
   >>> l.modified
   False
   >>> l.pop()
   2
   >>> l
   ModificationTrackingList([0, 1])
   >>> l.modified
   True


Class AliasedMultiDict
----------------------

class class kalamar.utils.AliasedMultiDict(data, aliases)

   MultiDict-like class using aliased keys.

   AliasedMultiDict is like a MultiDict, but using a dictionary of
   aliases available as AliasedMultiDict keys (in addition of the
   standard MultiDict keys).

   >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
   >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
   >>> aliasedmultidict = AliasedMultiDict(data, aliases)

   >>> aliasedmultidict['key1']
   'value1'
   >>> aliasedmultidict['alias1']
   'value1'
   >>> aliasedmultidict['key3']
   'value3'

   Note that: >>> issubclass(AliasedMultiDict, werkzeug.MultiDict)
   False

   get(key, default=None)

      Return ``self[key]`` if ``key`` in ``self``, else ``default``.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> aliasedmultidict.get('key1', 'test')
      'value1'
      >>> aliasedmultidict.get('alias1', 'test')
      'value1'
      >>> aliasedmultidict.get('alias8', 'test')
      'test'

   iterkeys()

      Return an iterator of high-level keys.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> sorted([key for key in aliasedmultidict.iterkeys()])
      ['alias1', 'alias2', 'key3']

   itervalues()

      Return an iterator of values.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> sorted([value for value in aliasedmultidict.itervalues()])
      ['value1', 'value2', 'value3']

   iteritems()

      Return an iterator of high-level (key, value) tuples.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> sorted([
      ...     (key, value) for (key, value) in aliasedmultidict.iteritems()])
      [('alias1', 'value1'), ('alias2', 'value2'), ('key3', 'value3')]

   keys()

      Return high-level keys.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> sorted(aliasedmultidict)
      ['alias1', 'alias2', 'key3']

   items()

      Return high-level (key, value) tuples.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> sorted(aliasedmultidict.items())
      [('alias1', 'value1'), ('alias2', 'value2'), ('key3', 'value3')]

   values()

      Return a list of values.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> sorted(aliasedmultidict.values())
      ['value1', 'value2', 'value3']

   popitem()

      Pop next item.

   clear()

      Empty ``self``.

      >>> aliases = {'alias1': 'key1', 'alias2': 'key2'}
      >>> data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
      >>> aliasedmultidict = AliasedMultiDict(data, aliases)

      >>> aliasedmultidict.clear()
      >>> aliasedmultidict.items()
      []

   update(other=(), **kwds)

      Update ``self`` with given ``other`` values.
