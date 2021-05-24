#!/usr/bin/env python

from lxml import etree

from .core import NEWSMLG2, NITF, NSMAP
from .newsitem import NewsItem

class NewsMLG2Document(object):
    _root_element = None
    newsitem = None

    def __init__(self, filename=None, string=None):
        if type(filename) == str:
            tree = etree.parse(filename)
            self._root_element = tree.getroot()
        elif type(string) == str or type(string) == bytes:
            self._root_element = etree.fromstring(string)

        if self._root_element.tag == NEWSMLG2+'newsItem':
            self.newsitem = NewsItem(
                xmlelement = self._root_element
            )
        else:
            raise Exception(
                "Item types other than NewsItem are not yet supported."
            )

    def getNewsItem(self):
        return self.newsitem

    def to_xml(self):
        elem = self.newsitem.to_xml()
        return etree.tostring(elem, pretty_print=True).decode()
