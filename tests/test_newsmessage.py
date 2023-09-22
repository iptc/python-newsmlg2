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
NewsML-G2 Python library - NewsMessage unit tests

"""

from lxml import etree
import os
import sys
import unittest
sys.path.append(os.getcwd())

import NewsMLG2

class TestNewsMLG2NewsItemStrings(unittest.TestCase):
    
    def test_parse_from_string(self):
        test_newsmlg2_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<newsMessage xmlns="http://iptc.org/std/nar/2006-10-01/">
    <header>
        <sent>2018-10-19T11:17:00.150Z</sent>
        <catalogRef href="http://www.example.com/std/catalog/NewsNessages_1.xml" />
        <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_32.xml" />
        <sender>thomsonreuters.com</sender>
        <transmitId>tag:reuters.com,2016:newsml_OVE48850O-PKG</transmitId>
        <priority>4</priority>
        <origin>MMS_3</origin>
        <destination role="nmdest:foobar">UKI</destination>
        <channel>TVS</channel>
        <channel>TTT</channel>
        <channel>WWW</channel>
        <timestamp role="received">2018-10-19T11:17:00.000Z</timestamp>
        <timestamp role="transmitted">2018-10-19T11:17:00.100Z</timestamp>
        <signal qcode="nmsig:atomic" />
    </header>
    <itemSet>
        <packageItem xmlns="http://iptc.org/std/nar/2006-10-01/"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     guid="news-message-example"
                     standard="NewsML-G2"
                     standardversion="2.32"
                     conformance="power"
                     xml:lang="en-GB">
            <itemMeta>
                <itemClass qcode="ninat:text"/>
                <provider uri="http://cv.iptc.org/newscodes/newsprovider/IPTC">
                    <name>IPTC</name>
                </provider>
                <versionCreated>2021-04-21T12:00:00+00:00</versionCreated>
                <firstCreated>2008-02-29T12:00:00+00:00</firstCreated>
                <pubStatus qcode="stat:usable"/>
            </itemMeta>
            <groupSet root="N1">
                <group>
                    <itemRef residref="N1" />
                </group>
            </groupSet>
        </packageItem>
        <newsItem
            xmlns="http://iptc.org/std/nar/2006-10-01/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            guid="N1"
            standard="NewsML-G2"
            standardversion="2.32"
            conformance="power"
            xml:lang="en-GB">
            <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_38.xml" />
            <itemMeta>
                <itemClass qcode="ninat:text"/>
                <provider uri="http://cv.iptc.org/newscodes/newsprovider/IPTC">
                    <name>IPTC</name>
                </provider>
                <versionCreated>2021-04-21T12:00:00+00:00</versionCreated>
                <firstCreated>2008-02-29T12:00:00+00:00</firstCreated>
                <pubStatus qcode="stat:usable"/>
            </itemMeta>
        </newsItem>
    </itemSet>
</newsMessage>
"""

        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)
        newsmessage = g2doc.get_item()
        header = newsmessage.header
        assert str(header.sent) == '2018-10-19T11:17:00.150Z'
        assert header.catalogref[0].href == 'http://www.example.com/std/catalog/NewsNessages_1.xml'
        assert header.catalogref[1].href == 'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_32.xml'
        assert str(header.sender) == 'thomsonreuters.com'
        assert str(header.transmitid) == 'tag:reuters.com,2016:newsml_OVE48850O-PKG'
        assert str(header.priority) == '4'
        assert str(header.origin) == 'MMS_3'
        assert header.destination.role == 'nmdest:foobar'
        assert str(header.destination) == 'UKI'
        assert str(header.channel[0]) == 'TVS'
        assert str(header.channel[1]) == 'TTT'
        assert str(header.channel[2]) == 'WWW'
        assert header.timestamp[0].role == 'received'
        assert str(header.timestamp[0]) == '2018-10-19T11:17:00.000Z'
        assert header.timestamp[1].role == 'transmitted'
        assert str(header.timestamp[1]) == '2018-10-19T11:17:00.100Z'
        assert header.signal.qcode == 'nmsig:atomic'

        itemset = newsmessage.itemset
        # itemset can't be tested right now as it's an xs:any construct which
        # we don't support yet.


class TestNewsMLG2NewsItemFiles(unittest.TestCase):
    def test_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '007_emptynewsmessage.xml')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        newsmessage = g2doc.get_item()
        header = newsmessage.header
        assert str(header.sent) == '2018-10-19T11:17:00.150Z'
        assert header.catalogref[0].href == 'http://www.example.com/std/catalog/NewsNessages_1.xml'
        assert header.catalogref[1].href == 'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_32.xml'
        assert str(header.sender) == 'thomsonreuters.com'
        assert str(header.transmitid) == 'tag:reuters.com,2016:newsml_OVE48850O-PKG'
        assert str(header.priority) == '4'
        assert str(header.origin) == 'MMS_3'
        assert header.destination.role == 'nmdest:foobar'
        assert str(header.destination) == 'UKI'
        assert str(header.channel[0]) == 'TVS'
        assert str(header.channel[1]) == 'TTT'
        assert str(header.channel[2]) == 'WWW'
        assert header.timestamp[0].role == 'received'
        assert str(header.timestamp[0]) == '2018-10-19T11:17:00.000Z'
        assert header.timestamp[1].role == 'transmitted'
        assert str(header.timestamp[1]) == '2018-10-19T11:17:00.100Z'
        assert header.signal.qcode == 'nmsig:atomic'

        itemset = newsmessage.itemset
        # itemset can't be tested right now as it's an xs:any construct which
        # we don't support yet.
