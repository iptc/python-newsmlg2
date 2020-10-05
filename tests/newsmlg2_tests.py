#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Copyright (c) 2020, IPTC
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
NewsML-G2 Python library - unit tests 

"""

import unittest
import os
import sys
sys.path.append(os.getcwd())

import NewsMLG2

XML_NS = '{http://www.w3.org/XML/1998/namespace}'

class TestStringMethods(unittest.TestCase):

    def test_parse_from_string(self):
        test_newsmlg2_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<newsItem
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    guid="simplest-test"
    standard="NewsML-G2"
    standardversion="2.29"
    conformance="power"
    version="1"
    xml:lang="en-GB">
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_35.xml" />
    <itemMeta>
        <itemClass qcode="ninat:text" />
        <provider qcode="nprov:IPTC" />
        <versionCreated>2020-06-22T12:00:00+03:00</versionCreated>
    </itemMeta>
    <contentSet>
        <inlineXML contenttype="application/nitf+xml">
        </inlineXML>
    </contentSet>
</newsItem>
"""
        parser = NewsMLG2.NewsMLG2Parser(string=test_newsmlg2_string)

        newsitem = parser.getNewsItem()
        assert newsitem.get_attr('guid') == 'simplest-test'
        assert newsitem.get_attr('standard') == 'NewsML-G2'
        assert newsitem.get_attr('standardversion') == '2.29'
        assert newsitem.get_attr('conformance') == 'power'
        assert newsitem.get_attr('version') == '1'
        assert newsitem.get_attr(XML_NS+'lang') == 'en-GB'

        catalog = newsitem.getCatalog()
        test_scheme = catalog.getSchemeForAlias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert test_scheme.definition == 'Indicates a company, publication or service provider.'

        # TODO tests on catalog
        assert newsitem.itemMeta.getItemClass() == 'ninat:text'
        # TODO convert qcode to URI
        # assert newsitem.itemMeta.getItemClassURI() == 'http://cv.iptc.org/newscodes/ninature/text'
        assert newsitem.itemMeta.getProvider() == 'nprov:IPTC'
        # TODO convert qcode to URI
        # assert newsitem.itemMeta.getProviderURI() == 'http://cv.iptc.org/newscodes/provider/IPTC'
        assert newsitem.itemMeta.versionCreated.getDateTime() == '2020-06-22T12:00:00+03:00'

    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '001_simplest_file.xml')
        parser = NewsMLG2.NewsMLG2Parser(filename=test_newsmlg2_file)
        newsitem = parser.getNewsItem()
        assert newsitem.get_attr('guid') == 'simplest-test-from-file'
        assert newsitem.get_attr('standard') == 'NewsML-G2'
        assert newsitem.get_attr('standardversion') == '2.29'
        assert newsitem.get_attr('conformance') == 'power'
        assert newsitem.get_attr(XML_NS+'lang') == 'en-GB'

        # catalog tests
        catalog = newsitem.getCatalog()
        test_scheme = catalog.getSchemeForAlias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert test_scheme.definition == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        assert newsitem.itemMeta.getItemClass() == 'ninat:text'
        # TODO convert qcode to URI
        # assert newsitem.itemMeta.getItemClassURI() == 'http://cv.iptc.org/newscodes/ninature/text'
        assert newsitem.itemMeta.getProvider() == 'nprov:IPTC'
        # TODO convert qcode to URI
        # assert newsitem.itemMeta.getProviderURI() == 'http://cv.iptc.org/newscodes/provider/IPTC'
        assert newsitem.itemMeta.versionCreated.getDateTime() == '2020-06-22T12:00:00+03:00'
        assert newsitem.contentSet.inlineXML.attr_values['contenttype'] == 'application/nitf+xml'

    def test_example_1(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', 'LISTING_1_A_NewsML-G2_News_Item.xml')
        parser = NewsMLG2.NewsMLG2Parser(filename=test_newsmlg2_file)

        newsitem = parser.getNewsItem()
        assert newsitem.get_attr('guid') == 'urn:newsml:acmenews.com:20161018:US-FINANCE-FED'
        assert newsitem.get_attr('standard') == 'NewsML-G2'
        assert newsitem.get_attr('standardversion') == '2.29'
        assert newsitem.get_attr('conformance') == 'power'
        assert newsitem.get_attr(XML_NS+'lang') == 'en-GB'
        assert newsitem.get_attr('version') == '11'

        rightsinfo = newsitem.rightsInfoArray[0]
        assert rightsinfo.copyrightHolder.attr_values['uri'] == 'http://www.example.com/about.html#copyright' 
        assert str(rightsinfo.copyrightHolder.names[0]) == 'Example Enews LLP'
        assert str(rightsinfo.copyrightNoticeArray) == 'Copyright 2017-18 Example Enews LLP, all rights reserved'
        assert str(rightsinfo.usageTermsArray) == 'Not for use outside the United States'

        itemmeta = newsitem.itemMeta
        assert newsitem.itemMeta.getItemClass() == 'ninat:text'
        # TODO convert qcode to URI
        # assert newsitem.itemMeta.getItemClassURI() == 'http://cv.iptc.org/newscodes/ninature/text'
        assert newsitem.itemMeta.getProvider() == 'nprov:REUTERS'
        # TODO convert qcode to URI
        # assert newsitem.itemMeta.getProviderURI() == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'

    <itemMeta>
        <itemClass qcode="ninat:text" />
        <provider qcode="nprov:REUTERS" />
        <versionCreated>2018-10-21T16:25:32-05:00</versionCreated>
        <firstCreated>2016-10-18T13:12:21-05:00</firstCreated>
        <embargoed>2018-10-23T12:00:00Z</embargoed>
      <pubStatus qcode="stat:usable" />
        <service qcode="svc:uknews">
            <name>UK News Service</name>
        </service>
        <edNote>
            Note to editors: STRICTLY EMBARGOED. Not for public release until 12noon
            on Friday, October 23, 2018.
        </edNote>
        <signal qcode="sig:update" />
        <link rel="irel:seeAlso"
            href="http://www.example.com/video/20081222-PNN-1517-407624/index.html"/>
    </itemMeta>

if __name__ == '__main__':
    unittest.main()
