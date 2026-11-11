#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
NewsML-G2 Python library - check that every catalog bundled with the module
loads from a catalogRef and resolves aliases

"""

import os
import sys
import unittest
sys.path.append(os.getcwd())

import NewsMLG2
from NewsMLG2.catalog import CATALOG_CACHE

ITEM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/" guid="catalog-test" standard="NewsML-G2" standardversion="2.36" conformance="power" version="1">
  <catalogRef href="{href}"/>
  <itemMeta>
    <itemClass qcode="ninat:text"/>
    <provider qcode="nprov:IPTC"/>
    <versionCreated>2026-11-11T09:00:00Z</versionCreated>
  </itemMeta>
</newsItem>
"""


def load_catalogs(href):
    g2doc = NewsMLG2.NewsMLG2Document(
        bytes(ITEM_TEMPLATE.format(href=href), 'utf-8')
    )
    return g2doc.get_item().get_catalogs()


class TestNewsMLG2CatalogCache(unittest.TestCase):

    def test_all_bundled_catalogs_load(self):
        for href in CATALOG_CACHE:
            with self.subTest(href=href):
                catalogs = load_catalogs(href)
                assert len(catalogs) == 1
                assert len(catalogs[0].scheme) > 0

    def test_catalog_v1_without_namespace(self):
        catalogs = load_catalogs(
            'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_1.xml'
        )
        scheme = catalogs.get_scheme_for_alias('acdc')
        assert scheme.uri == 'http://cv.iptc.org/newscodes/audiocodec/'

    def test_catalog_v42(self):
        catalogs = load_catalogs(
            'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_42.xml'
        )
        scheme = catalogs.get_scheme_for_alias('ninat')
        assert scheme.uri == 'http://cv.iptc.org/newscodes/ninature/'

    def test_sports_catalog_v2(self):
        catalogs = load_catalogs(
            'http://www.iptc.org/std/catalog/catalog.IPTC-Sports_2.xml'
        )
        scheme = catalogs.get_scheme_for_alias('spaward')
        assert scheme.uri == 'http://cv.iptc.org/newscodes/spaward/'


if __name__ == '__main__':
    unittest.main()
