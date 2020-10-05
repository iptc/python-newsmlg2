#!/usr/bin/env python

from lxml import etree

from .core import NEWSMLG2_NS, NITF_NS
from .newsitem import NewsItem

class NewsMLG2Parser(object):
    _root_element = None
    newsitem = None

    def __init__(self, filename=None, string=None):
        if type(filename) == str:
            tree = etree.parse(filename)
            self._root_element = tree.getroot()
        elif type(string) == str or type(string) == bytes:
            self._root_element = etree.fromstring(string)

        if self._root_element.tag == NEWSMLG2_NS+'newsItem':
            self.newsitem = NewsItem(
                xmlelement = self._root_element
            )
        else:
            raise Exception(
                " types other than NewsItem are not yet supported."
            )

    def getNewsItem(self):
        return self.newsitem
