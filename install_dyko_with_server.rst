=====================================
 Use Dyko with your dedicated server
=====================================


Dyko and Apache
==================

To use Dyko with Apache server, you just have to allow python script execution.

-----------
Preliminary
-----------

We are using a virtual host with the document root /var/www in this example.

---------------------
Installing mod_python
---------------------

To install mod_python, we simply run:


Ubuntu
------

Install package::


  apt-get install libapache2-mod-python

Enable module::

  a2enmod python


Restart Apache::

  sudo service apache2 restart

ArchLinux
---------

Install package::

  pacman -Sy mod_python

Enable module

Add this line to /etc/httpd/conf/httpd.conf::

  LoadModule python_module modules/mod_python.so

Restart Apache2::

  httpd -k restart

---------------------------
Utiliser les scripts python
---------------------------

Add those lines in  config file::

  <Directory /var/www>
  Options Indexes FollowSymLinks MultiViews
  AllowOverride None
  Order allow,deny
  allow from all
  
    AddHandler mod_python .py
    PythonHandler mod_python.publisher
    PythonDebug On
    
  </Directory>



Dyko and Lighttpd
=================

