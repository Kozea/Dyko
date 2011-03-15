JSONApi Tutorial
================

:abstract: This tutorial presents the JSON API offered by DykoX. It is
    experimental.


.. contents::



Installing DykoX
----------------

See the `dykoX documentation page </dykox#how-do-i-get-it>`_.

Using the API Server-side
-------------------------

The JSONRest interface is a simple WSGI middleware.

The simplest use-case is the following, assuming "site" is a kalamar site:

.. code-block:: python

    from kalamarx.jsonreststore.store import JSONRest

    my_wsgi_app = JSONRest(site)

This will expose the API at the root of your server. If you want to use it along
with an existing application, you can use the following code:

.. code-block:: python

    from kalamarx.jsonreststore.store import JSONRest

    my_wsgi_app = JSONRest(site, "/url_used_as_a_base/", existing_app)

The code above will expose the api on urls starting with "url_used_as_a_base",
routing other requests to existing_app.


Rest URLs
---------

The API follows the following conventions:

- Each access point is "mounted" at the root of the API. For example, if you
  have an access point registered as "my_db" on the kalamar site, it will be
  mounted on : /my_db/
- GET requests are used to retrieve items. A GET on the root of an access point
  will return every items from this access point.
- To get a specific item, append the item's identity properties (separated by
  slashes) to the access point name.
  For example, /my_db/1 will get the item from my db which identifier is "1"
- The POST method on an access point is used to create a new item. The POST body
  should contain the item in JSON format. For example, you would post the
  following date to create a new item in the my_db access_point:

.. code-block:: javascript

    {"id": 100,
     "firstname": "John",
     "lastname": "Doe"}

- The PUT method is used to update an item. Assuming you want to change the
  previously created item name, you would PUT the following data at /my_db/100:

.. code-block:: javascript

    {"id": 100,
     "firstname": "Robert"}

- The DELETE method is used to delete an item. Sending a DELETE request to
  /my_db/100 would delete the previously created item.


JSONQuery
---------

The API for searching kalamar items loosely follows the `JSONQuery specification 
<http://docs.persvr.org/documentation/jsonquery>`_.

GET requests on the access point will be translated in call to the view method
of the access point.


What is supported:

- Filters:

  * /my_db/?firstname='John' will return all items which firstname attribute is
    equal to John
  * /my_db/[?id>10] will return all items which id is greater than 10
  * /my_db/[? firstname='John' | id>10] will return all items which id is
    greater than ten OR which firstname is John
  * /my_db/[? firstname='John' & id>10] will return all items which id is
    greater than ten AND which firstname is John

- Orders:

  * /my_db/[/firstname] will return all items, sorted by ascending firstname
  * /my_db/[\firstname] will return all items, sorted by descending firstname
  * /my_db/[\firstname /id] will return all items, sorted by descending firstname
    and ascending id.

- Ranges:

  * /my_db/[/firstname][0:10] will return the first ten items, sorted by
    ascending firstname

- Retrieving specific attributes

  * /my_db/[={name: firstname}] will return every item firstname attribute,
    aliased as "name". It supports composed properties just like kalamar view
    method does.
- Distinct:

  * /my_db/[={name: firstname}].distinct() will return every distinct item firstname
    attribute, aliased as as ,name.






    


