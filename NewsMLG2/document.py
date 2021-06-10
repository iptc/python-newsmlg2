#!/usr/bin/env python

"""
Parent class to paarse a NewsMLG2 document.
"""

from lxml import etree

from .core import NEWSMLG2
from .newsitem import NewsItem

class NewsMLG2Document():
    """
    Parent class to paarse a NewsMLG2 document.
    """
    _root_element = None
    newsitem = None

    def __init__(self, filename=None, string=None):
        if isinstance(filename, str):
            tree = etree.parse(filename)
            self._root_element = tree.getroot()
        elif isinstance(string, (str, bytes)):
            self._root_element = etree.fromstring(string)

        if self._root_element.tag == NEWSMLG2+'newsItem':
            self.newsitem = NewsItem(
                xmlelement = self._root_element
            )
        else:
            raise Exception(
                "Item types other than NewsItem are not yet supported."
            )

    def get_newsitem(self):
        """Return the main NewsItem object for this document."""
        return self.newsitem

    def to_xml(self):
        """Return this document in XML form."""
        elem = self.newsitem.to_xml()
        return etree.tostring(elem, pretty_print=True).decode()
