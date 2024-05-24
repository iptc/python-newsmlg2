#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Copyright (c) 2021, IPTC
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

class TestNewsMLG2KnowledgeItems(unittest.TestCase):

    def test_parse_from_string(self):
        test_newsmlg2_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<knowledgeItem xmlns="http://iptc.org/std/nar/2006-10-01/" standard="NewsML-G2" standardversion="2.34" conformance="power" guid="urn:newsml:iptc.org:20080229:srcncdki-medtop-TS201901110952144" version="1">
  <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml"/>
  <rightsInfo>
    <copyrightHolder uri="http://cv.iptc.org/newscodes/newsprovider/IPTC">
      <name>IPTC - International Press Telecommunications Council</name>
    </copyrightHolder>
    <copyrightNotice>Copyright 2021, IPTC, www.iptc.org, Rights Reserved</copyrightNotice>
    <usageTerms href="http://creativecommons.org/licenses/by/4.0/">the Creative Commons Attribution (CC BY) 4.0 licence applies to all NewsCodes</usageTerms>
  </rightsInfo>
  <itemMeta>
    <itemClass qcode="cinat:scheme"/>
    <provider uri="http://cv.iptc.org/newscodes/newsprovider/IPTC">
      <name>IPTC</name>
    </provider>
    <versionCreated>2021-05-05T12:00:00+00:00</versionCreated>
    <firstCreated>2009-10-22T12:00:00+00:00</firstCreated>
    <pubStatus qcode="stat:usable"/>
  </itemMeta>
  <contentMeta>
    <contentCreated>2021-05-05T12:00:00+00:00</contentCreated>
    <description xml:lang="en-GB">Indicates a subject of an item.</description>
    <description xml:lang="en-GB">Media Topic</description>
  </contentMeta>
  <partMeta partid="pi1" contentrefs="medtop20000120 medtop20000345">
    <contentModified>2011-02-19T12:00:00+00:00</contentModified>
  </partMeta>
  <partMeta partid="pi2" contentrefs="medtop20000036 medtop20000037 medtop20000038 medtop20000039 medtop20000040 medtop20000042 medtop20000043 medtop20000044 medtop20000045 medtop20000168 medtop20000389 medtop20000393 medtop20000395 medtop20000619 medtop20000620 medtop20001124 medtop20001125 medtop20001126">
    <contentModified>2011-08-17T12:00:00+00:00</contentModified>
  </partMeta>
  <conceptSet>
    <concept id="nprovACCESSWIRE" modified="2021-02-09T12:00:00+00:00">
      <conceptId qcode="nprov:ACCESSWIRE" created="2021-02-09T12:00:00+00:00"/>
      <type qcode="cpnat:abstract"/>
      <name xml:lang="en-GB">ACCESSWIRE</name>
      <related uri="http://cv.iptc.org/newscodes/newsprovider/" rel="skos:inScheme"/>
    </concept>
    <concept id="nprovAFP" modified="2008-07-02T12:00:00+00:00">
      <conceptId qcode="nprov:AFP" created="2008-07-02T12:00:00+00:00"/>
      <type qcode="cpnat:abstract"/>
      <name xml:lang="en-GB">Agence France-Presse</name>
      <related uri="http://cv.iptc.org/newscodes/newsprovider/" rel="skos:inScheme"/>
    </concept>
    <concept id="nprovAMB" modified="2008-07-02T12:00:00+00:00">
      <conceptId qcode="nprov:AMB" created="2008-07-02T12:00:00+00:00"/>
      <type qcode="cpnat:abstract"/>
      <name xml:lang="en-GB">Associated MediaBase, Associated Newspapers Limited</name>
      <related uri="http://cv.iptc.org/newscodes/newsprovider/" rel="skos:inScheme"/>
    </concept>
    <concept id="nprovANA" modified="2008-07-02T12:00:00+00:00">
      <conceptId qcode="nprov:ANA" created="2008-07-02T12:00:00+00:00"/>
      <type qcode="cpnat:abstract"/>
      <name xml:lang="en-GB">Athens News Agency</name>
      <related uri="http://cv.iptc.org/newscodes/newsprovider/" rel="skos:inScheme"/>
    </concept>
  </conceptSet>
</knowledgeItem>
"""
        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)

        knowlitem = g2doc.get_item()
        assert knowlitem.guid == 'urn:newsml:iptc.org:20080229:srcncdki-medtop-TS201901110952144'
        assert knowlitem.standard == 'NewsML-G2'
        assert knowlitem.standardversion == '2.34'
        assert knowlitem.conformance == 'power'
        assert knowlitem.version == '1'

        catalogs = knowlitem.get_catalogs()
        # catalogs should work the same as for news items.
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = knowlitem.itemmeta
        assert itemmeta.itemclass.qcode == 'cinat:scheme'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/cinature/scheme'
        assert itemmeta.provider.uri == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert NewsMLG2.uri_to_qcode(itemmeta.provider.uri) == 'nprov:IPTC'
        assert str(itemmeta.versioncreated) == '2021-05-05T12:00:00+00:00'

        conceptset = knowlitem.conceptset
        assert conceptset.concept[0].id == 'nprovACCESSWIRE'
        assert conceptset.concept[0].modified == '2021-02-09T12:00:00+00:00'
        assert conceptset.concept[0].conceptid.qcode == 'nprov:ACCESSWIRE'
        assert NewsMLG2.qcode_to_uri(conceptset.concept[0].conceptid.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/ACCESSWIRE'
        assert conceptset.concept[0].conceptid.created == '2021-02-09T12:00:00+00:00'
        assert conceptset.concept[0].type.qcode == 'cpnat:abstract'
        assert NewsMLG2.qcode_to_uri(conceptset.concept[0].type.qcode) == 'http://cv.iptc.org/newscodes/cpnature/abstract'
        assert str(conceptset.concept[0].name) == 'ACCESSWIRE'
        assert conceptset.concept[0].name[0].xml_lang == 'en-GB'
        assert conceptset.concept[0].related.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert conceptset.concept[0].related.rel == 'skos:inScheme'

        assert conceptset.concept[1].id == 'nprovAFP'
        assert conceptset.concept[1].modified == '2008-07-02T12:00:00+00:00'
        assert conceptset.concept[1].conceptid.qcode == 'nprov:AFP'
        assert conceptset.concept[1].modified == '2008-07-02T12:00:00+00:00'
        assert conceptset.concept[1].type.qcode == 'cpnat:abstract'
        assert conceptset.concept[1].name[0].xml_lang == 'en-GB'
        assert str(conceptset.concept[1].name[0]) == 'Agence France-Presse'
        assert conceptset.concept[1].related.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert conceptset.concept[1].related.rel == 'skos:inScheme'


class TestNewsMLG2Files(unittest.TestCase):
    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '002_knowledgeitem.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        knowledgeitem = g2doc.get_item()
        assert knowledgeitem.guid == 'urn:newsml:iptc.org:20080229:srcncdki-nprov-TS202102091406532'
        assert knowledgeitem.standard == 'NewsML-G2'
        assert knowledgeitem.standardversion == '2.34'
        assert knowledgeitem.conformance == 'power'

        # catalog tests
        catalogs = knowledgeitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        itemmeta = knowledgeitem.itemmeta
        assert itemmeta.itemclass.qcode == 'cinat:scheme'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/cinature/scheme'
        assert itemmeta.provider.uri == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert NewsMLG2.uri_to_qcode(itemmeta.provider.uri) == 'nprov:IPTC'
        assert str(itemmeta.versioncreated) == '2021-04-21T12:00:00+00:00'

if __name__ == '__main__':
    unittest.main()
