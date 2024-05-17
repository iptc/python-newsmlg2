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

class TestNewsMLG2Events(unittest.TestCase):

    def test_parse_from_string(self):
        test_newsmlg2_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<conceptItem
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://iptc.org/std/nar/2006-10-01/
        ./NewsML-G2_2.32-spec-All-Power.xsd"
    guid="urn:newsml:iptc.org:20160422:qqwpiruuew4711"
    version="11"
    standard="NewsML-G2"
    standardversion="2.32"
    conformance="power"
    xml:lang="en">
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_38.xml" />
    <catalogRef href="http://www.example.com/events/event-catalog.xml" />
    <itemMeta>
        <itemClass qcode="cinat:concept" />
        <provider qcode="nprov:IPTC" />
        <versionCreated>2018-10-18T13:05:00Z</versionCreated>
        <pubStatus qcode="stat:usable" />
    </itemMeta>
    <contentMeta>
    <urgency>5</urgency>
    <contentCreated>2016-01-16T12:15:00Z</contentCreated>
    <contentModified>2018-06-12T13:35:00Z</contentModified>
    </contentMeta>
    <concept>
        <conceptId created="2018-01-16T12:15:00Z" qcode="event:1234567" />
        <type qcode="cpnat:event" />
        <name>IPTC Autumn Meeting 2018</name>
        <!-- eventDetails>
            <dates>
                <start>2018-10-26T09:00:00Z</start>
                <duration>P2D</duration>
            </dates>
            <location>
                <name>86, Edgeware Road, London W2 2EA, United Kingdom</name>
                <related rel="frel:venuetype" qcode="ventyp:confcentre" />
                <POIDetails>
                   <position latitude="51.515659" longitude="-0.163346" />
                   <contactInfo>
                       <web>https://www.etcvenues.co.uk</web>
                   </contactInfo>
                </POIDetails>
            </location>
            <participant qcode="eprol:director">
                <name>Michael Steidl</name>
                <personDetails>
                   <contactInfo>
                       <email>mdirector@iptc.org</email>
                   </contactInfo>
                </personDetails>
            </participant>
        </eventDetails -->
    </concept>
</conceptItem>
"""
        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)

        conceptitem = g2doc.get_item()
        assert conceptitem.guid == 'urn:newsml:iptc.org:20160422:qqwpiruuew4711'
        assert conceptitem.standard == 'NewsML-G2'
        assert conceptitem.standardversion == '2.32'
        assert conceptitem.conformance == 'power'
        assert conceptitem.version == '11'

        catalogs = conceptitem.get_catalogs()
        # catalogs should work the same as for news items.
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = conceptitem.itemmeta
        assert itemmeta.itemclass.qcode == 'cinat:concept'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/cinature/concept'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2018-10-18T13:05:00Z'

        concept = conceptitem.concept
        assert concept.conceptid.created == '2018-01-16T12:15:00Z'
        assert concept.conceptid.qcode == 'event:1234567'
    """
    <concept>
        <conceptId created="2018-01-16T12:15:00Z" qcode="event:1234567" />
        <type qcode="cpnat:event" />
        <name>IPTC Autumn Meeting 2018</name>
    """
 

class TestNewsMLG2EventFiles(unittest.TestCase):
    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '004_planningitem.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        planningitem = g2doc.get_item()
        assert planningitem.guid == 'urn:newsml:iptc.org:20211029:gbmdrmdreis4711'
        assert planningitem.standard == 'NewsML-G2'
        assert planningitem.standardversion == '2.34'
        assert planningitem.conformance == 'power'

        # catalog tests
        catalogs = planningitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        itemmeta = planningitem.itemmeta
        assert itemmeta.itemclass.qcode == 'plinat:newscoverage'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/plinature/newscoverage'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2021-10-29T12:45:00Z'

        assert planningitem.newscoverageset.newscoverage[0].id == 'ID_1234568'
        assert str(planningitem.newscoverageset.newscoverage[0].planning.ednote) == 'Text 250 words'
        assert planningitem.newscoverageset.newscoverage[1].id == 'ID_1234569'
        assert str(planningitem.newscoverageset.newscoverage[1].planning.ednote) == 'Picture scheduled 2018-12-25T12:0:00-05:00'
        # Note we can't check this (yet) because it's part of an xs:any section, it's not defined in the schema
        # assert planningitem.newscoverageset.newscoverage[1].delivery.delivereditemref.title == 'Henry Robinson pictured today in New York'


if __name__ == '__main__':
    unittest.main()
