#!/usr/bin/env python

"""
Parent class to paarse a NewsMLG2 document.
"""

from lxml import etree

from .core import NEWSMLG2NSPREFIX, NSMAP
from .conceptitem import ConceptItem
from .newsitem import NewsItem
from .knowledgeitem import KnowledgeItem

class NewsMLG2Document():
    """
    Parent class to paarse a NewsMLG2 document.
    """
    _root_element = None
    item = None

    def __init__(self, filename=None, string=None):
        if isinstance(filename, str):
            tree = etree.parse(filename)
            self._root_element = tree.getroot()
        elif isinstance(string, (str, bytes)):
            self._root_element = etree.fromstring(string)

        if self._root_element.tag == NEWSMLG2NSPREFIX+'newsItem':
            self.item = NewsItem(
                xmlelement = self._root_element
            )
        elif self._root_element.tag == NEWSMLG2NSPREFIX+'knowledgeItem':
            self.item = KnowledgeItem(
                xmlelement = self._root_element
            )
        elif self._root_element.tag == NEWSMLG2NSPREFIX+'conceptItem':
            self.item = ConceptItem(
                xmlelement = self._root_element
            )
        else:
            raise Exception(
                "Item types other than NewsItem and KnowledgeItem "
                "are not yet supported."
            )

    def get_item(self):
        """
        Return the main Item object (NewsItem, KnowledgeItem, ConceptItem etc)
        for this document.
        """
        return self.item

    def to_xml(self):
        """Return this document in XML form."""
        elem = self.item.to_xml()
        return etree.tostring(
                    elem,
                    pretty_print=True,
                    xml_declaration=True,
                    encoding='utf-8'
               #)
               ).decode('utf-8')
