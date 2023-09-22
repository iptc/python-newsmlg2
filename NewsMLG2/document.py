#!/usr/bin/env python

"""
Parent class to paarse a NewsMLG2 document.
"""

from lxml import etree

from .anyitem import AnyItem
from .core import NEWSMLG2NSPREFIX
from .catalogitem import CatalogItem
from .conceptitem import ConceptItem
from .knowledgeitem import KnowledgeItem
from .newsitem import NewsItem
from .newsmessage import NewsMessage
from .packageitem import PackageItem
from .planningitem import PlanningItem


class NewsMLG2Document():
    """
    Parent class to parse a NewsMLG2 document.
    """
    _root_element = None
    item = None

    def __init__(self, filename=None, string=None):
        if isinstance(filename, str):
            tree = etree.parse(filename)
            self._root_element = tree.getroot()
        elif isinstance(string, (str, bytes)):
            self._root_element = etree.fromstring(string)
        if self._root_element is not None:
            if self._root_element.tag == NEWSMLG2NSPREFIX+'catalogItem':
                self.item = CatalogItem(
                    xmlelement = self._root_element
                )
            elif self._root_element.tag == NEWSMLG2NSPREFIX+'conceptItem':
                self.item = ConceptItem(
                    xmlelement = self._root_element
                )
            elif self._root_element.tag == NEWSMLG2NSPREFIX+'knowledgeItem':
                self.item = KnowledgeItem(
                    xmlelement = self._root_element
                )
            elif self._root_element.tag == NEWSMLG2NSPREFIX+'newsItem':
                self.item = NewsItem(
                    xmlelement = self._root_element
                )
            elif self._root_element.tag == NEWSMLG2NSPREFIX+'packageItem':
                self.item = PackageItem(
                    xmlelement = self._root_element
                )
            elif self._root_element.tag == NEWSMLG2NSPREFIX+'planningItem':
                self.item = PlanningItem(
                    xmlelement = self._root_element
                )
            elif self._root_element.tag == NEWSMLG2NSPREFIX+'newsMessage':
                self.item = NewsMessage(
                    xmlelement = self._root_element
                )
            else:
                raise Exception(
                    "Root element is not a NewsML-G2 specified document root."
                )

    def get_item(self):
        """
        Return the main Item object (NewsItem, KnowledgeItem, ConceptItem etc)
        for this document.
        """
        return self.item

    def set_item(self, item):
        """
        Set the main Item object (NewsItem, KnowledgeItem, ConceptItem etc)
        for this document.
        """
        if not isinstance(item, AnyItem):
            raise Exception(
                "Item must be an instance of AnyItem (i.e. NewsItem, CatalogItem, "
                "ConceptItem, KnowledgeItem or PackageItem)"
            )
        self.item = item

    def to_xml(self):
        """Return this document in XML form."""
        elem = self.item.to_xml()
        return etree.tostring(
                    elem,
                    pretty_print=True,
                    xml_declaration=True,
                    encoding='utf-8'
               ).decode('utf-8')
