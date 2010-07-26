#!/usr/bin/env python
"""
Site'n'Co Main Script

"""

import os
import json
import kraken

import css


SITE_ROOT = os.path.dirname(__file__)
PROJECTS_PATH = os.path.join(SITE_ROOT, 'projects')
KALAMAR_CONF = os.path.join(SITE_ROOT, 'kalamar.conf')
CONFIG = {}

for project in os.listdir(PROJECTS_PATH):
    config_path = os.path.join(PROJECTS_PATH, project, 'configuration')
    CONFIG[project] = json.load(open(config_path))


class Site(kraken.Site):
    def _static(self, filename):
        fullpath = os.path.join(SITE_ROOT, filename)
        if not os.path.isfile(fullpath):
            raise kraken.utils.NotFound
        return kraken.utils.StaticFileResponse(fullpath)
     
    def handle_request(self, request):
        project_name = request.host.split('.')[-2]
        request.values = {'project_name': project_name}

        if request.path.startswith('/__static/'):
            return self._static(request.path.strip('/'))
        elif request.path.startswith('/src/'):
            return self._static(
                os.path.join('__static', request.path.strip('/')))
        elif request.path.startswith('/css/'):
            browser = request.path.split('/')[-1].rstrip('.css')
            return css.handle_request(request, browser, project_name)
        elif request.path.strip('/') == 'news':
            return self.template_response(
                request, 'news.html.jinja2', CONFIG[project_name], 
                'html', 'jinja2')
        else:
            request.values['page'] = request.path.strip('/')
            return self.template_response(
                request, 'page.html.jinja2', CONFIG[project_name],
                'html', 'jinja2')

    
if __name__ == '__main__':
    kraken.runserver(Site(site_root=SITE_ROOT, kalamar_conf=KALAMAR_CONF))
