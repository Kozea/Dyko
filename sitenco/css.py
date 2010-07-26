"""
C'n'Safe Support

"""

import os
import kraken

import cnsafe

def handle_request(request, browser, project_name):
    filename = os.path.join('__static', 'css', project_name, 'style.css')
    parser = cnsafe.Parser(filename)
    browser_parser = getattr(cnsafe, browser)
    return kraken.utils.Response(
        repr(browser_parser.transform(parser, keep_existant=False)),
        headers={'Content-Type': 'text/css'})
