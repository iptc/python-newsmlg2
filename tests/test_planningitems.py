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

class TestNewsMLG2PlanningItems(unittest.TestCase):

    def test_parse_from_string(self):
        test_newsmlg2_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<planningItem 
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://iptc.org/std/nar/2006-10-01/
        ./NewsML-G2_2.34-spec-All-Power.xsd"
    guid="urn:newsml:iptc.org:20101025:gbmrmdreis4711"
    version="11"
    standard="NewsML-G2"
    standardversion="2.34"
    conformance="power"
    xml:lang="en">
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml" />
    <catalogRef href="http://www.example.com/events/event-catalog.xml" />
    <itemMeta>
        <itemClass qcode="plinat:newscoverage" />
        <provider qcode="nprov:IPTC" />
        <versionCreated>2018-10-18T13:45:00Z
        </versionCreated>
        <pubStatus qcode="stat:usable" />
    </itemMeta>
    <contentMeta>
        <urgency>5</urgency>
        <contentCreated>2015-10-16T12:15:00Z</contentCreated>
        <contentModified>2018-10-16T13:35:00Z</contentModified>
        <headline>The 12 Days of Christmas</headline>
    </contentMeta>
    <newsCoverageSet>
        <newsCoverage id="ID_1234568" modified="2018-09-26T13:19:11Z">
           <planning>
               <g2contentType>application/nitf+xml</g2contentType>
               <itemClass qcode="ninat:text"/>
               <assignedTo
                   coversfrom="2018-12-24T06:00:00Z"
                   coversto="2018-12-24T23:00:00Z"
                   qcode="santastaff:ceo">
                   <name>Chief Elf Officer</name>
               </assignedTo>
               <scheduled>2018-12-24T23:30:00Z</scheduled>
               <headline>All Wrapped Up in Lapland</headline>
               <edNote>Text 250 words</edNote>
           </planning>
           <planning>
               <g2contentType>application/nitf+xml</g2contentType>
               <itemClass qcode="ninat:text"/>
               <assignedTo
                   coversfrom="2018-12-24T23:00:00Z"
                   coversto="2018-12-25T12:00:00Z"
                   qcode="santastaff:santa">
                   <name>Santa Claus</name>
               </assignedTo>
               <scheduled>2018-12-25T06:30:00Z</scheduled>
               <headline>Santa's Sleigh Ride</headline>
               <edNote>Text 250 words</edNote>
           </planning>
        </newsCoverage>
        <newsCoverage id="ID_1234569" modified="2018-09-26T15:19:11Z">
           <planning>
               <g2contentType>image/jpeg</g2contentType>
               <itemClass qcode="ninat:picture"></itemClass>
               <scheduled>2018-12-25T00:00:00Z</scheduled>
               <edNote>Picture will be Santa Claus departing with reindeer</edNote>
           </planning>
        </newsCoverage>
    </newsCoverageSet>
</planningItem>
"""
        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)

        planningitem = g2doc.get_item()
        assert planningitem.guid == 'urn:newsml:iptc.org:20101025:gbmrmdreis4711'
        assert planningitem.standard == 'NewsML-G2'
        assert planningitem.standardversion == '2.34'
        assert planningitem.conformance == 'power'
        assert planningitem.version == '11'

        catalogs = planningitem.get_catalogs()
        # catalogs should work the same as for news items.
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = planningitem.itemmeta
        assert itemmeta.itemclass.qcode == 'plinat:newscoverage'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/plinature/newscoverage'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2018-10-18T13:45:00Z'

        assert len(planningitem.newscoverageset.newscoverage) == 2

        newscoverage = planningitem.newscoverageset.newscoverage[0]
        assert newscoverage.id == 'ID_1234568'
        assert newscoverage.modified == '2018-09-26T13:19:11Z'

        planning = newscoverage.planning[0]
        assert str(planning.g2contenttype) == 'application/nitf+xml'
        assert planning.itemclass.qcode == 'ninat:text'
        assert NewsMLG2.qcode_to_uri(planning.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/text'
        assert planning.assignedto.coversfrom == '2018-12-24T06:00:00Z'
        assert planning.assignedto.coversto == '2018-12-24T23:00:00Z'
        assert planning.assignedto.qcode == 'santastaff:ceo'
        assert str(planning.assignedto.name) == 'Chief Elf Officer'
        assert str(planning.scheduled) == '2018-12-24T23:30:00Z'
        assert str(planning.headline) == 'All Wrapped Up in Lapland'
        assert str(planning.ednote) == 'Text 250 words'

        planning2 = newscoverage.planning[1]
        assert str(planning2.g2contenttype) == 'application/nitf+xml'
        assert planning2.itemclass.qcode == 'ninat:text'
        assert NewsMLG2.qcode_to_uri(planning2.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/text'
        assert planning2.assignedto.coversfrom == '2018-12-24T23:00:00Z'
        assert planning2.assignedto.coversto == '2018-12-25T12:00:00Z'
        assert planning2.assignedto.qcode == 'santastaff:santa'
        assert str(planning2.assignedto.name) == 'Santa Claus'
        assert str(planning2.scheduled) == '2018-12-25T06:30:00Z'
        assert str(planning2.headline) == 'Santa\'s Sleigh Ride'
        assert str(planning2.ednote) == 'Text 250 words'

        newscoverage2 = planningitem.newscoverageset.newscoverage[1]
        newscoverage2.id == 'ID_1234569'
        newscoverage2.modified == '2018-09-26T15:19:11Z'

        planning3 = newscoverage2.planning
        assert str(planning3.g2contenttype) == 'image/jpeg'
        assert planning3.itemclass.qcode == 'ninat:picture'
        assert NewsMLG2.qcode_to_uri(planning3.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/picture'
        assert str(planning3.scheduled) == '2018-12-25T00:00:00Z'
        assert str(planning3.ednote) == 'Picture will be Santa Claus departing with reindeer'


class TestNewsMLG2Files(unittest.TestCase):
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
