=====
DykoX
=====

What is DykoX ?
===============

DykoX contains (at the time this is being written) additional access points and
a JSON Rest API.

Currently, the additional access points are:

- kalamarx.access_point.geocoding.GeoCoder: An access point (read-only) to the
  Google GeoCoding API

- kalamarx.access_point.radicale.CalDav: An access point to access calendars and
  events on a CalDav server. Currently only tested against `Radicale <http://radicale.org>`_.


How do I get it ?
=================


DykoX is hosted on :codelink:`GitHub`, on the DykoX branch.
Clone the repository, and run the setup script (as root): 

.. code-block:: bash

    git clone git://github.com/Kozea/Dyko.git
    git checkout dykox
    sudo setup.py install


What is the JSON Rest API you mentioned earlier?
================================================

There is a simple documentation `there </jsonapi/>`_.
