**************
Dyko - Kalamar
**************

Kalamar is an object-relational mapping library for the `Python`_ language. Its concept is based on our called "access-point".  

Site
====
.. autoclass:: kalamar.Site
    :members:
    
Item
====
.. automodule:: kalamar.item

Class Item
----------
.. autoclass:: Item
    :members:
    
Parser
======

Class TextItem
--------------
.. autoclass:: kalamar.parser.textitem.TextItem

Class RestAtom
--------------
.. autoclass:: kalamar.parser.rest.RestAtom

Class RestCapsule
-----------------
.. autoclass:: kalamar.parser.rest.RestCapsule

Class MessageItem
-----------------
.. autoclass:: kalamar.parser.mail.MessageItem

Class OneToManyDBCapsule
------------------------
.. autoclass:: kalamar.parser.db_capsule.OneToManyDBCapsule

Class ManyToManyDBCapsule
-------------------------
.. autoclass:: kalamar.parser.db_capsule.ManyToManyDBCapsule

Class GenericManyToManyDBCapsule
--------------------------------
.. autoclass:: kalamar.parser.db_capsule.GenericManyToManyDBCapsule 

Storage
=======

Class AccessPoint
-----------------

.. automodule:: kalamar.storage.base

.. autoclass:: AccessPoint
    :members:

Class DBAPIStorage
------------------

.. automodule:: kalamar.storage.dbapi

.. autoclass:: DBAPIStorage

Class FileSystemStorage
-----------------------

.. automodule:: kalamar.storage.filesystem

.. autoclass:: FileSystemStorage

Class MySQLdbStorage
-----------------------

.. automodule:: kalamar.storage.mysqldb

.. autoclass:: MySQLdbStorage

Class PostgreSQLStorage
-----------------------

.. automodule:: kalamar.storage.postgresql

.. autoclass:: PostgreSQLStorage

Class SQLiteStorage
-----------------------

.. automodule:: kalamar.storage.sqlite

.. autoclass:: SQLiteStorage


Utils
=====

.. automodule:: kalamar.utils
    :members: apply_to_result,
	      re_match,
	      re_not_match,
	      recursive_subclasses,
	      simple_cache
	      
Class OperatorNotAvailable 	      
--------------------------	      
.. autoclass:: OperatorNotAvailable

Class ParserNotAvailable 	      
------------------------	
.. autoclass:: ParserNotAvailable

Class Condition 	      
---------------
.. autoclass:: Condition

Class ModificationTrackingList 	      
------------------------------
.. autoclass:: ModificationTrackingList
    :members: modifies
    
Class AliasedMultiDict 	      
----------------------    
.. autoclass:: AliasedMultiDict
    :members: reversed_aliases,
	          get,
	          iterkeys,
	          itervalues,
	          iteritems,
	          keys,
	          items,
	          values,
	          popitem,
	          clear,
	          update
	      
        
.. _Python: http://www.python.org
