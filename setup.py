#!/usr/bin/env python

# Public Domain

from setuptools import setup, find_packages

setup(
    name = 'Dykox',
    version = '0.2.dev1',
    packages = find_packages(
        exclude=['*._test', '*._test.*', 'test.*', 'test']),
    package_dir = {
        'kalamarx' : 'kalamarx'
    },
    package_data = {
        '': ['AUTHORS'],
        'doc': ['*.rst']
    },
    install_requires = [
        'dyko>=0.2.dev1'
    ],
    extras_require = {
        'Radicale': ['radicale>=0.5'],
        'jsonreststore' : ['ply>=3.3']
    },
    author = "Kozea",
    author_email = "ronan.dunklau@kozea.fr",
    description = "This is a set of various extensions to dyko",
    license = "GPL",
    keywords = "web framework caldav json rest plugins",
    url = "http://www.dyko.org/",
    zip_safe=False)
