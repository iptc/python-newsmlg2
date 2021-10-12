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
NewsML-G2 Python library - NewsItem unit tests 

"""

from lxml import etree
import os
import sys
import unittest
sys.path.append(os.getcwd())

import NewsMLG2

XML_NS = '{http://www.w3.org/XML/1998/namespace}'

class TestNewsMLG2NewsItemStrings(unittest.TestCase):

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
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml" />
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

        newsitem = g2doc.get_item()
        assert newsitem.guid == 'simplest-test'
        assert newsitem.standard == 'NewsML-G2'
        assert newsitem.standardversion == '2.29'
        assert newsitem.conformance == 'power'
        assert newsitem.version == '1'
        assert newsitem.xml_lang == 'en-GB'

        catalogs = newsitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('prov')
        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/provider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a company, publication or service provider.'

        itemmeta = newsitem.itemmeta
        assert itemmeta.itemclass.qcode == 'ninat:text'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/text'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2020-06-22T12:00:00+03:00'

class TestNewsMLG2NewsItemFiles(unittest.TestCase):
    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '001_simplest_file.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        newsitem = g2doc.get_item()
        assert newsitem.guid == 'simplest-test-from-file'
        assert newsitem.standard == 'NewsML-G2'
        assert newsitem.standardversion == '2.29'
        assert newsitem.conformance == 'power'
        assert newsitem.xml_lang == 'en-GB'

        # catalog tests
        catalogs = newsitem.get_catalogs()
        test_scheme = catalogs.get_scheme_for_alias('nprov')

        assert test_scheme.uri == 'http://cv.iptc.org/newscodes/newsprovider/'
        assert test_scheme.authority == 'https://iptc.org/'
        assert test_scheme.modified == '2019-09-13T12:00:00+00:00'
        assert str(test_scheme.definition) == 'Indicates a News Provider registered with the IPTC.'

        # itemmeta tests
        itemmeta = newsitem.itemmeta
        assert itemmeta.itemclass.qcode == 'ninat:text'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/text'
        assert itemmeta.provider.qcode == 'nprov:IPTC'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
        assert str(itemmeta.versioncreated) == '2020-06-22T12:00:00+03:00'
        assert newsitem.contentset.inlinexml.contenttype == 'application/nitf+xml'

    def test_example_1_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', 'LISTING_1_A_NewsML-G2_News_Item.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)

        newsitem = g2doc.get_item()
        assert newsitem.guid == 'urn:newsml:acmenews.com:20161018:US-FINANCE-FED'
        assert newsitem.standard == 'NewsML-G2'
        assert newsitem.standardversion == '2.29'
        assert newsitem.conformance == 'power'
        assert newsitem.xml_lang == 'en-GB'
        assert newsitem.version == '11'

        rightsinfo = newsitem.rightsinfo
        assert rightsinfo.copyrightholder.uri == 'http://www.example.com/about.html#copyright' 
        assert str(rightsinfo.copyrightholder.name) == 'Example Enews LLP'
        assert str(rightsinfo.copyrightnotice) == 'Copyright 2017-18 Example Enews LLP, all rights reserved'
        assert str(rightsinfo.copyrightnotice) == 'Copyright 2017-18 Example Enews LLP, all rights reserved'
        assert str(rightsinfo.usageterms) == 'Not for use outside the United States'

        itemmeta = newsitem.itemmeta
        assert itemmeta.itemclass.qcode == 'ninat:text'
        assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/text'
        assert itemmeta.provider.qcode == 'nprov:REUTERS'
        assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/REUTERS'
        assert str(itemmeta.versioncreated) == '2018-10-21T16:25:32-05:00'
        assert str(itemmeta.firstcreated) == '2016-10-18T13:12:21-05:00'
        assert str(itemmeta.embargoed) == '2018-10-23T12:00:00Z'
        # TODO some test like isEmbargoed?? isPublishable??
        assert itemmeta.pubstatus.qcode == 'stat:usable'
        assert NewsMLG2.qcode_to_uri(itemmeta.pubstatus.qcode) == 'http://cv.iptc.org/newscodes/pubstatusg2/usable'
        assert itemmeta.service.qcode == 'svc:uknews'
        # alias 'svc' is not in our catalog, so this raises an exception
        with self.assertRaises(NewsMLG2.AliasNotFoundInCatalogs):
            assert NewsMLG2.qcode_to_uri(itemmeta.service.qcode) == ''
        assert str(itemmeta.service.name) == 'UK News Service'
        assert str(itemmeta.ednote) == 'Note to editors: STRICTLY EMBARGOED. Not for public release until 12noon on Friday, October 23, 2018.'
        assert itemmeta.signal.qcode == 'sig:update'
        assert NewsMLG2.qcode_to_uri(itemmeta.signal.qcode) == 'http://cv.iptc.org/newscodes/signal/update'
        assert itemmeta.link.rel == 'irel:seeAlso'
        assert NewsMLG2.qcode_to_uri(itemmeta.link.rel) == 'http://cv.iptc.org/newscodes/itemrelation/seeAlso'
        assert itemmeta.link.href == 'http://www.example.com/video/20081222-PNN-1517-407624/index.html'

        contentmeta = newsitem.contentmeta
        assert str(contentmeta.contentcreated) == '2016-10-18T11:12:00-05:00'
        assert str(contentmeta.contentmodified) == '2018-10-21T16:22:45-05:00'
        assert contentmeta.located.type == 'cptype:city'
        assert contentmeta.located.qcode == 'geo:345678'
        assert str(contentmeta.located.name) == 'Berlin'
        assert contentmeta.located.broader[0].type == 'cptype:statprov'
        assert contentmeta.located.broader[0].qcode == 'prov:2365'
        assert str(contentmeta.located.broader[0].name) == 'Berlin'
        assert contentmeta.located.broader[1].type == 'cptype:country'
        assert contentmeta.located.broader[1].qcode == 'iso3166-1a2:DE'
        assert str(contentmeta.located.broader[1].name) == 'Germany'

        # test GenericArray iterator code in NewsMLG2/core.py
        broadernames = [str(broader.name) for broader in contentmeta.located.broader]
        assert broadernames == ['Berlin', 'Germany']

        assert contentmeta.creator.uri == 'http://www.example.com/staff/mjameson'
        assert str(contentmeta.creator.name) == 'Meredith Jameson'
        assert contentmeta.infosource.uri == 'http://www.example.com'
        assert contentmeta.subject[0].type == 'cpnat:abstract'
        assert contentmeta.subject[0].qcode == 'medtop:04000000'
        assert contentmeta.subject[0].name[0].get_attr('xml_lang') == 'en-GB'
        assert contentmeta.subject[0].name[0].xml_lang == 'en-GB'
        assert str(contentmeta.subject[0].name) == 'economy, business and finance'
        assert contentmeta.subject[1].type == 'cpnat:abstract'
        assert contentmeta.subject[1].qcode == 'medtop:20000523'
        assert str(contentmeta.subject[1].name[0]) == 'labour market'
        assert contentmeta.subject[1].name[0].get_attr('xml_lang') == 'en-GB'
        assert str(contentmeta.subject[1].name[1]) == 'Arbeitsmarkt'
        assert contentmeta.subject[1].name[1].get_attr('xml_lang') == 'de'
        assert contentmeta.subject[1].broader.qcode == 'medtop:04000000'

        # Helper function to get available language versions
        assert contentmeta.subject[1].name.get_languages() == ['en-GB', 'de']
        # Helper function to get a given language version
        assert contentmeta.subject[1].name.get_language('en-GB') == 'labour market'
        assert contentmeta.subject[1].name.get_language('de') == 'Arbeitsmarkt'

        assert contentmeta.genre.qcode == 'genre:interview'
        assert str(contentmeta.genre.name) == 'Interview'
        assert contentmeta.genre.name[0].get_attr('xml_lang') == 'en-GB'
        assert str(contentmeta.slugline) == 'US-Finance-Fed'
        assert str(contentmeta.headline) == 'Fed to halt QE to avert "bubble"'

        assert newsitem.contentset.inlinexml.contenttype == 'application/nitf+xml'

    def test_example_3_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', 'LISTING_3_Photo_in_NewsML-G2.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)

        newsitem = g2doc.get_item()
        assert newsitem.guid == 'tag:gettyimages.com,2010:GYI0062134533'
        assert newsitem.version == '11'
        assert newsitem.standard == 'NewsML-G2'
        assert newsitem.standardversion == '2.29'
        assert newsitem.conformance == 'power'
        assert newsitem.get_attr('xml_lang') == 'en-US'
        # catalog tests??
        # <catalogRef
        #     href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_32.xml" />
        # <catalogRef href="http://cv.gettyimages.com/nml2catalog4customers-1.xml" />
        assert newsitem.rightsinfo.copyrightholder.uri == 'http://www.gettyimages.com'
        assert str(newsitem.rightsinfo.copyrightholder.name) == 'Getty Images North America'
        assert newsitem.rightsinfo.copyrightnotice.href == 'http://www.gettyimages.com/Corporate/LicenseInfo.aspx'
        assert str(newsitem.rightsinfo.copyrightnotice) == 'Copyright 2010 Getty Images. -- http://www.gettyimages.com/Corporate/LicenseInfo.aspx'
        assert str(newsitem.rightsinfo.usageterms) == (
                'Contact your local office for all commercial or '
                'promotional uses. Full editorial rights UK, US, Ireland, Canada (not '
                'Quebec). Restricted editorial rights for daily newspapers elsewhere, '
                'please call.'
        )
        assert str(newsitem.contentmeta.creditline) == 'Getty Images'
        assert newsitem.contentmeta.subject[0].type == 'cpnat:event'
        assert newsitem.contentmeta.subject[0].qcode == 'gyimeid:104530187'
        assert newsitem.contentmeta.subject[1].type == 'cpnat:abstract'
        assert newsitem.contentmeta.subject[1].qcode == 'medtop:20000523'
        assert newsitem.contentmeta.subject[1].name[0].get_attr('xml_lang') == 'en-GB'
        assert str(newsitem.contentmeta.subject[1].name[0]) == 'labour market'
        assert newsitem.contentmeta.subject[1].name[1].get_attr('xml_lang') == 'de'
        assert str(newsitem.contentmeta.subject[1].name[1]) == 'Arbeitsmarkt'
        assert newsitem.contentmeta.subject[2].type == 'cpnat:abstract'
        assert newsitem.contentmeta.subject[2].qcode == 'medtop:20000533'
        assert newsitem.contentmeta.subject[2].name[0].get_attr('xml_lang') == 'en-GB'
        assert str(newsitem.contentmeta.subject[2].name[0]) == 'unemployment'
        assert newsitem.contentmeta.subject[2].name[1].get_attr('xml_lang') == 'de'
        assert str(newsitem.contentmeta.subject[2].name[1]) == 'Arbeitslosigkeit'
        assert newsitem.contentmeta.subject[3].type == 'cpnat:geoArea'
        assert str(newsitem.contentmeta.subject[3].name) == 'Las Vegas Boulevard'

        assert newsitem.contentmeta.subject[4].type == 'cpnat:geoArea'
        assert newsitem.contentmeta.subject[4].qcode == 'gycon:89109'
        assert str(newsitem.contentmeta.subject[4].name) == 'Las Vegas'
        assert newsitem.contentmeta.subject[4].broader[0].qcode == 'iso3166-1a2:US-NV'
        assert str(newsitem.contentmeta.subject[4].broader[0].name) == 'Nevada'
        assert newsitem.contentmeta.subject[4].broader[1].qcode == 'iso3166-1a3:USA'
        assert str(newsitem.contentmeta.subject[4].broader[1].name) == 'United States'
        [str(keyword) for keyword in newsitem.contentmeta.keyword] == [
            'business', 'economic', 'economy', 'finance', 'poor', 'poverty', 'gamble'
        ] 
        assert str(newsitem.contentmeta.headline) == 'Variety Of Recessionary Forces Leave Las Vegas Economy Scarred'
        assert newsitem.contentmeta.description.role == 'drol:caption'
        assert str(newsitem.contentmeta.description) == (
            'A general view of part of downtown, '
            'including Las Vegas Boulevard, on October 20, 2010 in Las Vegas, '
            'Nevada. Nevada once had among the lowest unemployment rates in the '
            'United States at 3.8 percent but has since fallen on difficult times. '
            'Las Vegas, the gaming capital of America, has been especially hard '
            'hit with unemployment currently at 14.7 percent and the highest '
            'foreclosure rate in the nation. Among the sparkling hotels and '
            'casinos downtown are dozens of dormant construction projects and '
            'hotels offering rock bottom rates. As the rest of the country slowly '
            'begins to see some economic progress, Las Vegas is still in the midst '
            'of the economic downturn. (Photo by Spencer Platt/Getty Images)'
        )

class TestNewsMLG2NewsItemFromCode(unittest.TestCase):
    def test_create_simple_newsitem_in_code(self):
        g2doc = NewsMLG2.NewsMLG2Document()
        newsitem = NewsMLG2.NewsItem()
        newsitem.guid = 'test-guid'
        newsitem.xml_lang = 'en-GB'
        g2doc.set_item(newsitem)

        output_newsitem = g2doc.get_item()
        assert newsitem.guid == 'test-guid'
        assert newsitem.standard == 'NewsML-G2'
        assert newsitem.standardversion == '2.29'
        assert newsitem.conformance == 'power'
        assert newsitem.version == '1'
        assert newsitem.xml_lang == 'en-GB'
        
    def test_create_newsitem_in_code_with_no_guid_fails(self):
        g2doc = NewsMLG2.NewsMLG2Document()
        newsitem = NewsMLG2.NewsItem()
        g2doc.set_item(newsitem)

        output_newsitem = g2doc.get_item()

        with self.assertRaises(AttributeError):
            output_xml = g2doc.to_xml()

    def test_toxml_from_code(self):
        g2doc = NewsMLG2.NewsMLG2Document()
        newsitem = NewsMLG2.NewsItem()
        newsitem.guid = 'test-guid'
        newsitem.xml_lang = 'en-GB'
        g2doc.set_item(newsitem)

        output_xml = g2doc.to_xml()
        assert output_xml == ('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n'
                              '<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/" xmlns:nitf="http://iptc.org/std/NITF/2006-10-18/" xml:lang="en-GB" standard="NewsML-G2" standardversion="2.29" conformance="power" guid="test-guid" version="1"/>\n')

    def test_create_valid_newsitem_in_code(self):
        g2doc = NewsMLG2.NewsMLG2Document()
        newsitem = NewsMLG2.NewsItem()
        newsitem.guid = 'test-guid'
        newsitem.xml_lang = 'en-GB'
        itemmeta = NewsMLG2.ItemMeta()
        itemmeta.itemclass.qcode = "ninat:text"
        itemmeta.provider.qcode = "nprov:IPTC"
        itemmeta.versioncreated = "2020-06-22T12:00:00+03:00"
        newsitem.itemmeta = itemmeta
        g2doc.set_item(newsitem)

        output_newsitem = g2doc.get_item()
        assert newsitem.guid == 'test-guid'
        assert newsitem.standard == 'NewsML-G2'
        assert newsitem.standardversion == '2.29'
        assert newsitem.conformance == 'power'
        assert newsitem.version == '1'
        assert newsitem.xml_lang == 'en-GB'

        output_xml = g2doc.to_xml()
        assert output_xml == ("<?xml version='1.0' encoding='utf-8'?>\n"
                              '<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/" xmlns:nitf="http://iptc.org/std/NITF/2006-10-18/" xml:lang="en-GB" standard="NewsML-G2" standardversion="2.29" conformance="power" guid="test-guid" version="1">\n'
                              '  <itemMeta>\n'
                              '    <itemClass qcode="ninat:text"/>\n'
                              '    <provider qcode="nprov:IPTC"/>\n'
                              '    <versionCreated>2020-06-22T12:00:00+03:00</versionCreated>\n'
                              '  </itemMeta>\n'
                              '</newsItem>\n')

 
if __name__ == '__main__':
    unittest.main()
