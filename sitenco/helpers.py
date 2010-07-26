"""
Various Helpers

"""

import docutils.core
import docutils.writers.html4css1
import ConfigParser
import datetime
from xml.etree import ElementTree


def rest_to_article(item, level=3):
    """Convert ``item`` to HTML article."""
    parts = docutils.core.publish_parts(
        source=item['text'],
        writer=docutils.writers.html4css1.Writer(),
        settings_overrides={'initial_header_level': level})

    # Post-production modification of generated document
    text = parts['html_body']
    # Escaping non-breaking spaces is a strange behavior in docutils, a TODO
    # exists in docutils.writers.html4css1.HTMLTranslator.encode. ElementTree
    # does not like &nbsp; so we change it by the real unicode chacarter.
    text = text.replace('&nbsp;', u'\xa0')
    tree = ElementTree.fromstring(text.encode('utf-8'))
    for element in tree.getiterator():
        if element.tag == 'div' and element.get('class') == 'document':
            element.tag = 'article'
        elif element.tag == 'tt':
            element.tag = 'code'
        elif element.tag == 'tbody':
            if 'valign' in element.attrib:
                del element.attrib['valign']
        elif element.tag == 'div' and element.get('class') == 'section':
            element.tag = 'section'
        elif element.tag == 'h1' and element.get('class') == 'title':
            element.tag = 'h%i' % (level - 1)

        for attrib in ('frame', 'rules', 'border', 'width', 'valign'):
            if attrib in element.attrib:
                del element.attrib[attrib]
        
    return ElementTree.tostring(tree)


def pretty_datetime(datetime_string):
    return datetime.datetime.strptime(
        datetime_string,'%Y-%m-%d@%H:%M:%S').strftime('%A, %B %-d %Y')
