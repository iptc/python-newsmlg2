#!/usr/bin/env python

import argparse
import os
import sys

# because we want to reference a module that hasn't been installed yet
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..'))

from NewsMLG2 import NewsMLG2Document

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load NewsML-G2 instance file')
    parser.add_argument('filename', help='file to be loaded')
    args = parser.parse_args()

    """
    if type(args.filename) == str:
        tree = None
        tree = etree.parse(args.filename)
        self._root_element = tree.getroot()
        if self._root_element.tag == NEWSMLG2_NS+'newsItem':
            self.newsitem = NewsItem(
                xmlelement = self._root_element
            )
        else:
            raise Exception(
                " types other than NewsItem are not yet supported."
            )
    else:
        raise Exception("filename should be a string")
    """
    document = NewsMLG2Document(args.filename)

    # news_item = parser.getNewsItem()
    print(document.to_xml())
