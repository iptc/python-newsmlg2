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

class TestNewsMLG2Strings(unittest.TestCase):

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
        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)

        newsitem = g2doc.get_newsitem()
        assert newsitem.get_attr('guid') == 'simplest-test'
        assert newsitem.get_attr('standard') == 'NewsML-G2'
        assert newsitem.get_attr('standardversion') == '2.29'
        assert newsitem.get_attr('conformance') == 'power'
        assert newsitem.get_attr('version') == '1'
        assert newsitem.get_attr(XML_NS+'lang') == 'en-GB'

        catalogs = newsitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert test_scheme.definition == 'Indicates a company, publication or service provider.'

        item_meta = newsitem.get_itemmeta()
        assert item_meta.get_itemclass() == 'ninat:text'
        assert item_meta.get_itemclass_uri() == 'http://cv.iptc.org/newscodes/ninature/text'
        assert item_meta.get_provider() == 'nprov:IPTC'
        assert item_meta.get_provider_uri() == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert item_meta.get_versioncreated() == '2020-06-22T12:00:00+03:00'

class TestNewsMLG2Files(unittest.TestCase):
    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '001_simplest_file.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        newsitem = g2doc.get_newsitem()
        assert newsitem.get_attr('guid') == 'simplest-test-from-file'
        assert newsitem.get_attr('standard') == 'NewsML-G2'
        assert newsitem.get_attr('standardversion') == '2.29'
        assert newsitem.get_attr('conformance') == 'power'
        assert newsitem.get_attr(XML_NS+'lang') == 'en-GB'

        # catalog tests
        catalogs = newsitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert test_scheme.definition == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        item_meta = newsitem.get_itemmeta()
        assert item_meta.get_itemclass() == 'ninat:text'
        assert item_meta.get_itemclass_uri() == 'http://cv.iptc.org/newscodes/ninature/text'
        assert item_meta.get_provider() == 'nprov:IPTC'
        assert item_meta.get_provider_uri() == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert item_meta.get_versioncreated() == '2020-06-22T12:00:00+03:00'
        assert newsitem.contentSet.inlineXML.attr_values['contenttype'] == 'application/nitf+xml'

    def test_example_1_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', 'LISTING_1_A_NewsML-G2_News_Item.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)

        newsitem = g2doc.get_newsitem()
        assert newsitem.get_attr('guid') == 'urn:newsml:acmenews.com:20161018:US-FINANCE-FED'
        assert newsitem.get_attr('standard') == 'NewsML-G2'
        assert newsitem.get_attr('standardversion') == '2.29'
        assert newsitem.get_attr('conformance') == 'power'
        assert newsitem.get_attr(XML_NS+'lang') == 'en-GB'
        assert newsitem.get_attr('version') == '11'

        rightsinfo = newsitem.get_rightsinfo()[0]
        assert rightsinfo.get_copyrightholder().attr_values['uri'] == 'http://www.example.com/about.html#copyright' 
        assert str(rightsinfo.get_copyrightholder().names[0]) == 'Example Enews LLP'
        assert str(rightsinfo.get_copyrightnotice()[0]) == 'Copyright 2017-18 Example Enews LLP, all rights reserved'
        assert str(rightsinfo.get_copyrightnotice()[0]) == 'Copyright 2017-18 Example Enews LLP, all rights reserved'
        assert str(rightsinfo.get_usageterms()) == 'Not for use outside the United States'

        item_meta = newsitem.get_itemmeta()
        assert item_meta.get_itemclass() == 'ninat:text'
        assert item_meta.get_itemclass_uri() == 'http://cv.iptc.org/newscodes/ninature/text'
        assert item_meta.get_provider() == 'nprov:REUTERS'
        assert item_meta.get_provider_uri() == 'http://cv.iptc.org/newscodes/newsprovider/REUTERS'
        assert item_meta.get_versioncreated() == '2018-10-21T16:25:32-05:00'
        assert item_meta.get_firstcreated() == '2016-10-18T13:12:21-05:00'
        assert item_meta.get_embargoed() == '2018-10-23T12:00:00Z'
        # TODO some test like isEmbargoed?? isPublishable??
        assert item_meta.get_pubstatus() == 'stat:usable'
        assert item_meta.get_pubstatus_uri() == 'http://cv.iptc.org/newscodes/pubstatusg2/usable'
        assert item_meta.get_service() == 'svc:uknews'
        # alias 'svc' is not in our catalog, so this raises an exception
        with self.assertRaises(NewsMLG2.AliasNotFoundInCatalogs):
            assert item_meta.get_service_uri() == ''
        assert item_meta.get_services()[0].get_name()[0].name == 'UK News Service'
        #assert item_meta.ednote == 'Note to editors: STRICTLY EMBARGOED. Not for public release until 12noon on Friday, October 23, 2018.'
        #assert item_meta.get_signal() == 'sig:update'
        #assert item_meta.get_signal_uri() == 'http://cv.iptc.org/newscodes/sig/update'
        #assert item_meta.links[0].get_rel() == 'irel:seeAlso'
        #assert item_meta.links[0].get_rel_uri() == 'http://cv.iptc.org/newscodes/irel/seeAlso'
        #assert item_meta.links[0].href == 'http://www.example.com/video/20081222-PNN-1517-407624/index.html'

    """
    TODO...
    <contentMeta>
        <contentCreated>2016-10-18T11:12:00-05:00</contentCreated>
        <contentModified>2018-10-21T16:22:45-05:00</contentModified>
        <located type="cptype:city" qcode="geo:345678">
            <name>Berlin</name>
            <broader type="cptype:statprov" qcode="prov:2365">
                <name>Berlin</name>
            </broader>
            <broader type="cptype:country" qcode="iso3166-1a2:DE">
                <name>Germany</name>
            </broader>
        </located>
        <creator uri="http://www.example.com/staff/mjameson" >
            <name>Meredith Jameson</name>
        </creator>
        <infoSource uri="http://www.example.com" />
        <subject type="cpnat:abstract" qcode="medtop:04000000">
            <name xml:lang="en-GB">economy, business and finance</name>
        </subject>
        <subject type="cpnat:abstract" qcode="medtop:20000523">
            <name xml:lang="en-GB">labour market</name>
            <name xml:lang="de">Arbeitsmarkt</name>
            <broader qcode="medtop:04000000" />
        </subject>
        <genre qcode="genre:interview">
            <name xml:lang="en-GB">Interview</name>
        </genre>
        <slugline>US-Finance-Fed</slugline>
        <headline> Fed to halt QE to avert "bubble"</headline>
    </contentMeta>
    """

if __name__ == '__main__':
    unittest.main()
