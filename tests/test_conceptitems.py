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


class TestNewsMLG2ConceptItems(unittest.TestCase):

    def test_parse_conceptitem_from_string(self):
        test_newsmlg2_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<conceptItem
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:other="http://other.com/other-namespace"
    guid="conceptitem-string-test"
    standard="NewsML-G2"
    standardversion="2.24"
    conformance="power"
    xml:lang="en-GB">
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml"/>
    <itemMeta>
        <itemClass qcode="cinat:concept"/>
        <provider literal="reuters.com"/>
        <versionCreated>2019-09-09T08:00:00.000Z</versionCreated>
    </itemMeta>
    <concept>
        <conceptId qcode="P:111"/>
        <type qcode="cptType:37"/>
        <name>Event111:Name</name>
        <eventDetails>
            <!-- WHEN -->
            <dates>
                <start confirmationstatus="edconf:approximate">2016-06-25T10:00:00Z</start>
                <end confirmationstatus="edconf:undefined">2016</end>
                <!-- DEPRECATED: Use @confirmationstatus -->
                <confirmation qcode="edconf:bothApprox"/>
            </dates>
        </eventDetails>
    </concept>
</conceptItem>
"""
        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)

        conceptitem = g2doc.get_item()
        assert conceptitem.guid == 'conceptitem-string-test'
        assert conceptitem.standard == 'NewsML-G2'
        assert conceptitem.standardversion == '2.24'
        assert conceptitem.conformance == 'power'
        assert conceptitem.version == '1'
        assert conceptitem.xml_lang == 'en-GB'

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
        assert itemmeta.provider.literal == 'reuters.com'
        assert str(itemmeta.versioncreated) == '2019-09-09T08:00:00.000Z'

        concept = conceptitem.concept
        assert concept.conceptid.qcode == 'P:111'
        assert concept.type.qcode == 'cptType:37'
        assert str(concept.name) == 'Event111:Name'

        # TODO test eventDetails section

class TestNewsMLG2ConceptItemFiles(unittest.TestCase):
    def test_parse_conceptitem_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '003_conceptitem.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        conceptitem = g2doc.get_item()
        assert conceptitem.guid == '003-concept-item-file-test'
        assert conceptitem.standard == 'NewsML-G2'
        assert conceptitem.standardversion == '2.34'
        assert conceptitem.conformance == 'power'

        # catalog tests
        catalogs = conceptitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        itemmeta = conceptitem.itemmeta
        assert itemmeta.itemclass.qcode == 'cinat:concept'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/cinature/concept'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2020-06-22T12:00:00+03:00'

    def test_parse_conceptitem_with_persondetails_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '005_conceptitem_persondetails.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        conceptitem = g2doc.get_item()
        assert conceptitem.guid == 'urn:newsml:iptc.org:005-conceptitem-with-persondetails-test'
        assert conceptitem.standard == 'NewsML-G2'
        assert conceptitem.standardversion == '2.34'
        assert conceptitem.conformance == 'power'

        # catalog tests
        catalogs = conceptitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        itemmeta = conceptitem.itemmeta
        assert itemmeta.itemclass.qcode == 'cinat:concept'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/cinature/concept'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2018-11-07T12:38:18Z'

        # concept tests
        concept = conceptitem.concept
        assert concept.conceptid.qcode == 'people:329465'
        assert concept.type.qcode == 'cpnat:person'
        assert str(concept.name) == 'Mario Draghi'
        assert concept.definition.role == 'definitionrole:biog'
        assert str(concept.definition).startswith('Mario Draghi, born 3 September 1947,') == True
        assert concept.note.role == 'nrol:disambiguation'
        assert str(concept.note) == 'Not Mario D’roggia, international powerboat racer'
        assert concept.related.rel == 'relation:occupation'
        assert concept.related.qcode == 'jobtypes:puboff'
        assert concept.sameas.type == 'cpnat:person'
        assert concept.sameas.qcode == 'pers:567223'
        assert str(concept.sameas.name) == 'DRAGHI, Mario'

        persondetails = concept.persondetails
        assert str(persondetails.born) == '1947-09-03'
        assert persondetails.affiliation.type == 'orgnat:employer'
        assert persondetails.affiliation.qcode == 'org:ECB'
        assert str(persondetails.affiliation.name) == 'European Central Bank'

        contactinfo = concept.persondetails.contactinfo
        assert contactinfo.email.role == 'ciprol:office'
        assert str(contactinfo.email) == 'info@ecb.eu'
        assert contactinfo.im.role == 'imsrvc:reuters'
        assert str(contactinfo.im) == 'president.ecb.eu@reuters.net'
        assert len(contactinfo.phone) == 2
        assert contactinfo.phone[0].role == 'ciprol:office'
        assert str(contactinfo.phone[0]) == '+49 69 13 44 0'
        assert contactinfo.phone[1].role == 'ciprol:mobile'
        assert str(contactinfo.phone[1]) == '+49 69 13 44 60 00'
        assert str(contactinfo.web) == 'www.ecb.eu'
        assert contactinfo.address.role == 'ciprol:office'
        assert str(contactinfo.address.line) == 'Kaiserstrasse 29'
        assert str(contactinfo.address.locality.name) == 'Frankfurt am Main'
        assert contactinfo.address.country.qcode == 'iso3166-1a2:DE'
        assert str(contactinfo.address.country.name) == 'Germany'
        assert str(contactinfo.address.postalcode) == 'D-60311'

    def test_parse_conceptitem_with_geoareadetails_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '006_conceptitem_geoareadetails.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        conceptitem = g2doc.get_item()
        assert conceptitem.guid == 'urn:newsml:iptc.org:006-conceptitem-with-geoareadetails-test'
        assert conceptitem.standard == 'NewsML-G2'
        assert conceptitem.standardversion == '2.34'
        assert conceptitem.conformance == 'power'

        # catalog tests
        catalogs = conceptitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        itemmeta = conceptitem.itemmeta
        assert itemmeta.itemclass.qcode == 'cinat:concept'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/cinature/concept'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2023-07-19T12:00:00Z'
        assert str(itemmeta.title) == 'Concept Item describing Kentucky'

        # concept tests
        concept = conceptitem.concept
        assert concept.conceptid.qcode == 'apgeography:2f6e294082b310048474df092526b43e'
        assert concept.type.qcode == 'cpnat:geoArea'
        assert str(concept.name) == 'Kentucky'

        geoareadetails = concept.geoareadetails
        assert geoareadetails.position.latitude == '-84.87762'
        assert geoareadetails.position.longitude == '38.20042'
        assert str(geoareadetails.founded) == '1792-06-01'
        # just to test the element! not a prediction :-)
        assert str(geoareadetails.dissolved) == '2099-12-31'
        assert geoareadetails.polygon.position[0].latitude == '-89.57291911219112'
        assert geoareadetails.polygon.position[0].longitude == '36.49707311372113'
        assert geoareadetails.polygon.position[1].latitude == '-81.96720514115141'
        assert geoareadetails.polygon.position[1].longitude == '39.14641319952199'


if __name__ == '__main__':
    unittest.main()
