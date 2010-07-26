#!/usr/bin/env python
"""
FCGI Script for Launching Site'n'Co

"""

from flup.server.fcgi import WSGIServer

import sitenco

WSGIServer(sitenco.Site(
        site_root=sitenco.SITE_ROOT, kalamar_conf=sitenco.KALAMAR_CONF)).run()
