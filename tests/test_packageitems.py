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

class TestNewsMLG2PackageItems(unittest.TestCase):

    def test_parse_from_string(self):
        test_newsmlg2_string = """<?xml version="1.0" encoding="UTF-8"?>
<packageItem
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://iptc.org/std/nar/2006-10-01/
        ./NewsML-G2_2.34-spec-All-Power.xsd"
     standard="NewsML-G2"
    standardversion="2.34"
    conformance="power"
    guid="tag:example.com,2008:UK-NEWS-TOPTEN:UK20081220098658" version="11">
    <catalogRef
        href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml" />
    <catalogRef
        href="http:/www.example.com/customer/cv/catalog4customers-1.xml" />
    <itemMeta>
        <itemClass qcode="ninat:composite" />
        <provider qcode="nprov:IPTC" />
        <versionCreated>2018-11-17T12:30:00Z</versionCreated>
        <firstCreated>2008-12-20T12:25:35Z</firstCreated>
        <pubStatus qcode="stat:usable" />
        <profile versioninfo="1.0.0.2">simple_text_with_picture.xsl</profile>
        <service qcode="svc:uktop">
            <name>Top UK News stories hourly</name>
        </service>
        <title>UK-TOPNEWS</title>
        <edNote>Updates the previous version</edNote>
        <signal qcode="sig:update" />
    </itemMeta>
    <contentMeta>
        <contributor jobtitle="staffjobs:cpe" qcode="mystaff:MDancer">
            <name>Maurice Dancer</name>
            <name>Chief Packaging Editor</name>
            <definition validto="2018-11-17T17:30:00Z">
                Duty Packaging Editor
            </definition>
            <note validto="2018-11-17T17:30:00Z">
                Available on +44 207 345 4567 until 17:30 GMT today
            </note>
        </contributor>
         <headline xml:lang="en">UK</headline>
    </contentMeta>
    <groupSet root="G1">
        <group id="G1" role="group:main">
            <itemRef residref="urn:newsml:iptc.org:20081007:tutorial-item-A"
                contenttype="application/vnd.iptc.g2.newsitem+xml"
                size="2345">
                <itemClass qcode="ninat:text" />
                <provider qcode="nprov:AcmeNews"/>
                <pubStatus qcode="stat:usable"/>
                <title>Obama annonce son équipe</title>
                <description role="drol:summary">Le rachat il y a deux ans de la
                   propriété par Alan Gerry, magnat local de la télévision câblée, a
                   permis l'investissement des 100 millions de dollars qui étaient
                   nécessaires pour le musée et ses annexes, et vise à favoriser le
                   développement touristique d'une région frappée par le chômage.
                </description>
            </itemRef>
            <itemRef residref="urn:newsml:iptc.org:20081007:tutorial-item-B"
                contenttype="application/vnd.iptc.g2.newsitem+xml"
                size="300039">
                <itemClass qcode="ninat:picture" />
                <provider qcode="nprov:AcmeNews"/>
                <pubStatus qcode="stat:usable"/>
                <title>Barack Obama arrive à Washington</title>
                <description role="drol:caption">Si nous avons aujourd'hui un
                   afro-américain et une femme dans la course à la présidence.
                </description>
            </itemRef>
        </group>
    </groupSet>
</packageItem>""".encode('utf-8')

        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)

        packageitem = g2doc.get_item()
        assert packageitem.guid == 'tag:example.com,2008:UK-NEWS-TOPTEN:UK20081220098658'
        assert packageitem.standard == 'NewsML-G2'
        assert packageitem.standardversion == '2.34'
        assert packageitem.conformance == 'power'
        assert packageitem.version == '11'

        catalogs = packageitem.get_catalogs()
        # catalogs should work the same as for news items.
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = packageitem.itemmeta
        assert itemmeta.itemclass.qcode == 'ninat:composite'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/composite'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2018-11-17T12:30:00Z'
        assert str(itemmeta.firstcreated) == '2008-12-20T12:25:35Z'
        assert itemmeta.pubstatus.qcode == 'stat:usable'
        assert NewsMLG2.qcode_to_uri(itemmeta.pubstatus.qcode) == 'http://cv.iptc.org/newscodes/pubstatusg2/usable'
        assert itemmeta.profile.versioninfo == '1.0.0.2'
        assert str(itemmeta.profile) == 'simple_text_with_picture.xsl'
        assert itemmeta.service.qcode == 'svc:uktop'
        assert str(itemmeta.service.name) == 'Top UK News stories hourly'
        assert str(itemmeta.title) == 'UK-TOPNEWS'
        assert str(itemmeta.ednote) == 'Updates the previous version'
        assert itemmeta.signal.qcode == 'sig:update'

        contentmeta = packageitem.contentmeta
        assert contentmeta.contributor.jobtitle == 'staffjobs:cpe'
        assert contentmeta.contributor.qcode == 'mystaff:MDancer'
        assert str(contentmeta.contributor.name[0]) == 'Maurice Dancer'
        assert str(contentmeta.contributor.name[1]) == 'Chief Packaging Editor'
        assert contentmeta.contributor.definition.validto == '2018-11-17T17:30:00Z'
        assert str(contentmeta.contributor.definition) == 'Duty Packaging Editor'
        assert contentmeta.contributor.note.validto == '2018-11-17T17:30:00Z'
        assert str(contentmeta.contributor.note) == 'Available on +44 207 345 4567 until 17:30 GMT today'
        assert str(contentmeta.headline) == 'UK'
        assert contentmeta.headline.xml_lang == 'en'

        groupset = packageitem.groupset
        assert groupset.root == 'G1'
        # TODO rootGroup = packageitem.getRootGroup(); assert rootGroup == groupset.group[0]
        assert groupset.group[0].id == 'G1'
        assert groupset.group[0].role == 'group:main'
        itemref0 = groupset.group[0].itemref[0]
        assert itemref0.residref == 'urn:newsml:iptc.org:20081007:tutorial-item-A'
        assert itemref0.contenttype == 'application/vnd.iptc.g2.newsitem+xml'
        assert itemref0.size == '2345'  # TODO should this become an integer?
        # the below fields only work because of xs:any under itemRef, should we support those??
        #assert itemref0.itemclass.qcode == 'ninat:text'
        #assert itemref0.provider.qcode == 'nprov:AcmeNews'
        #assert itemref0.pubstatus.qcode == 'stat:usable'
        #assert str(itemref0.title) == 'Obama annonce son équipe'
        #assert itemref0.description.role == 'drol:summary'
        #assert str(itemref0.description).startswith('Le rachat il y a deux ans de la')
        itemref1 = groupset.group[0].itemref[1]
        assert itemref1.residref == 'urn:newsml:iptc.org:20081007:tutorial-item-B'
        assert itemref1.contenttype == 'application/vnd.iptc.g2.newsitem+xml'
        assert itemref1.size == '300039'  # TODO should this become an integer?
        # the below fields only work because of xs:any under itemRef, should we support those??
        #assert itemref1.itemclass.qcode == 'ninat:picture'
        #assert itemref1.provider.qcode == 'nprov:AcmeNews'
        #assert itemref1.pubstatus.qcode == 'stat:usable'
        #assert str(itemref1.title) == 'Barack Obama arrive à Washington'
        #assert itemref1.description.role == 'drol:caption'
        #assert str(itemref1.description).startswith('Si nous avons aujourd\'hui un')


class TestNewsMLG2Files(unittest.TestCase):
    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', 'LISTING_6_Simple_NewsML-G2_Package.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        packageitem = g2doc.get_item()
        assert packageitem.guid == 'tag:example.com,2008:UK-NEWS-TOPTEN:UK20081220098658'
        assert packageitem.standard == 'NewsML-G2'
        assert packageitem.standardversion == '2.34'
        assert packageitem.conformance == 'power'
        assert packageitem.version == '11'

        catalogs = packageitem.get_catalogs()
        # catalogs should work the same as for news items.
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = packageitem.itemmeta
        assert itemmeta.itemclass.qcode == 'ninat:composite'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/composite'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2018-11-17T12:30:00Z'
        assert str(itemmeta.firstcreated) == '2008-12-20T12:25:35Z'
        assert itemmeta.pubstatus.qcode == 'stat:usable'
        assert NewsMLG2.qcode_to_uri(itemmeta.pubstatus.qcode) == 'http://cv.iptc.org/newscodes/pubstatusg2/usable'
        assert itemmeta.profile.versioninfo == '1.0.0.2'
        assert str(itemmeta.profile) == 'simple_text_with_picture.xsl'
        assert itemmeta.service.qcode == 'svc:uktop'
        assert str(itemmeta.service.name) == 'Top UK News stories hourly'
        assert str(itemmeta.title) == 'UK-TOPNEWS'
        assert str(itemmeta.ednote) == 'Updates the previous version'
        assert itemmeta.signal.qcode == 'sig:update'

        contentmeta = packageitem.contentmeta
        assert contentmeta.contributor.jobtitle == 'staffjobs:cpe'
        assert contentmeta.contributor.qcode == 'mystaff:MDancer'
        assert str(contentmeta.contributor.name[0]) == 'Maurice Dancer'
        assert str(contentmeta.contributor.name[1]) == 'Chief Packaging Editor'
        assert contentmeta.contributor.definition.validto == '2018-11-17T17:30:00Z'
        assert str(contentmeta.contributor.definition) == 'Duty Packaging Editor'
        assert contentmeta.contributor.note.validto == '2018-11-17T17:30:00Z'
        assert str(contentmeta.contributor.note) == 'Available on +44 207 345 4567 until 17:30 GMT today'
        assert str(contentmeta.headline) == 'UK'
        assert contentmeta.headline.xml_lang == 'en'

        groupset = packageitem.groupset
        assert groupset.root == 'G1'
        # TODO rootGroup = packageitem.getRootGroup(); assert rootGroup == groupset.group[0]
        assert groupset.group[0].id == 'G1'
        assert groupset.group[0].role == 'group:main'
        itemref0 = groupset.group[0].itemref[0]
        assert itemref0.residref == 'urn:newsml:iptc.org:20081007:tutorial-item-A'
        assert itemref0.contenttype == 'application/vnd.iptc.g2.newsitem+xml'
        assert itemref0.size == '2345'  # TODO should this become an integer?
        # the below fields only work because of xs:any under itemRef, should we support those??
        #assert itemref0.itemclass.qcode == 'ninat:text'
        #assert itemref0.provider.qcode == 'nprov:AcmeNews'
        #assert itemref0.pubstatus.qcode == 'stat:usable'
        #assert str(itemref0.title) == 'Obama annonce son équipe'
        #assert itemref0.description.role == 'drol:summary'
        #assert str(itemref0.description).startswith('Le rachat il y a deux ans de la')
        itemref1 = groupset.group[0].itemref[1]
        assert itemref1.residref == 'urn:newsml:iptc.org:20081007:tutorial-item-B'
        assert itemref1.contenttype == 'application/vnd.iptc.g2.newsitem+xml'
        assert itemref1.size == '300039'  # TODO should this become an integer?
        # the below fields only work because of xs:any under itemRef, should we support those??
        #assert itemref1.itemclass.qcode == 'ninat:picture'
        #assert itemref1.provider.qcode == 'nprov:AcmeNews'
        #assert itemref1.pubstatus.qcode == 'stat:usable'
        #assert str(itemref1.title) == 'Barack Obama arrive à Washington'
        #assert itemref1.description.role == 'drol:caption'
        #assert str(itemref1.description).startswith('Si nous avons aujourd\'hui un')


if __name__ == '__main__':
    unittest.main()
