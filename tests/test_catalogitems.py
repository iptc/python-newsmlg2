#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Copyright (c) 2022, IPTC
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

class TestNewsMLG2CatalogItems(unittest.TestCase):

    def test_parse_from_string(self):
        # LISTING_13 example
        test_newsmlg2_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<catalogItem
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://iptc.org/std/nar/2006-10-01/
        ./NewsML-G2_2.34-spec-All-Power.xsd"
    guid="urn:newsml:iptc.org:20130517:catalog"
    version="31"
    standard="NewsML-G2"
    standardversion="2.34"
    conformance="power"
    xml:lang="en-GB">
    <catalogRef
        href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml" />
    <rightsInfo>
        <copyrightHolder uri="http://www.iptc.org">
            <name>IPTC</name>
        </copyrightHolder>
    </rightsInfo>
    <itemMeta>
        <itemClass qcode="catinat:catalog" />
        <provider qcode="nprov:IPTC">
            <name>International Press Telecommunications Council</name>
        </provider>
        <versionCreated>2018-10-17T12:00:00Z</versionCreated>
        <pubStatus qcode="stat:usable" />
    </itemMeta>
    <catalogContainer>
        <catalog xmlns="http://iptc.org/std/nar/2006-10-01/"
            additionalInfo="http://www.iptc.org/goto?G2cataloginfo">
            <scheme alias="app" uri="http://cv.iptc.org/newscodes/application/">
                <definition xml:lang="en-GB">Indicates how the metadata
                   value was applied.</definition>
                <name xml:lang="en-GB">Application of Metadata Values</name>
            </scheme>
            <scheme alias="foo" uri="http://cv.iptc.org/newscodes/foo/">
                <definition xml:lang="en-GB">Indicates how the metadata
                   value was applied.</definition>
                <name xml:lang="en-GB">Application of Metadata Values</name>
            </scheme>
        </catalog>
    </catalogContainer>
</catalogItem>
"""
        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)

        catitem = g2doc.get_item()
        assert catitem.guid == 'urn:newsml:iptc.org:20130517:catalog'
        assert catitem.standard == 'NewsML-G2'
        assert catitem.standardversion == '2.34'
        assert catitem.conformance == 'power'
        assert catitem.version == '31'

        catalogs = catitem.get_catalogs()
        # catalogs should work the same as for news items.
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = catitem.itemmeta
        assert str(itemmeta.itemclass.qcode) == 'catinat:catalog'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/catinature/catalog'
        assert str(itemmeta.provider.qcode) == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2018-10-17T12:00:00Z'

        catalog = catitem.catalogcontainer.catalog
        assert catalog.additionalinfo == 'http://www.iptc.org/goto?G2cataloginfo'
        scheme = catalog.scheme[0]
        assert scheme.alias == 'app'
        assert scheme.uri == 'http://cv.iptc.org/newscodes/application/'
        assert scheme.definition.xml_lang == 'en-GB'
        assert str(scheme.definition) == 'Indicates how the metadata value was applied.'
        assert scheme.name.xml_lang == 'en-GB'
        assert str(scheme.name) == 'Application of Metadata Values'


class TestNewsMLG2CatalogItemFiles(unittest.TestCase):
    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', 'LISTING_13_Complete_Catalog_Item.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        catitem = g2doc.get_item()
        assert catitem.guid == 'urn:newsml:iptc.org:20130517:catalog'
        assert catitem.standard == 'NewsML-G2'
        assert catitem.standardversion == '2.34'
        assert catitem.conformance == 'power'
        assert catitem.version == '31'

        catalogs = catitem.get_catalogs()
        # catalogs should work the same as for news items.
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = catitem.itemmeta
        assert itemmeta.itemclass.qcode == 'catinat:catalog'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/catinature/catalog'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2018-10-17T12:00:00Z'

        catalog = catitem.catalogcontainer.catalog
        assert catalog.additionalinfo == 'http://www.iptc.org/goto?G2cataloginfo'
        scheme = catalog.scheme[0]
        assert scheme.alias == 'app'
        assert scheme.uri == 'http://cv.iptc.org/newscodes/application/'
        assert scheme.definition.xml_lang == 'en-GB'
        assert str(scheme.definition) == 'Indicates how the metadata value was applied.'
        assert scheme.name.xml_lang == 'en-GB'
        assert str(scheme.name) == 'Application of Metadata Values'

if __name__ == '__main__':
    unittest.main()
