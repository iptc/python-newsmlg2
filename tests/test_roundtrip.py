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

class TestNewsMLG2Roundtrip(unittest.TestCase):
    """
    Test roundtrip on examples:
    If we load a NewsML-G2 document into our library, then use the to_xml() feature to
    output the same file again, they should match.
    """

    def test_roundtrip_from_string(self):
        test_newsmlg2_string = b"""<?xml version='1.0' encoding='utf-8'?>
<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/" xmlns:nitf="http://iptc.org/std/NITF/2006-10-18/" xml:lang="en-GB" standard="NewsML-G2" standardversion="2.34" conformance="power" guid="simplest-test" version="1">
  <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_38.xml"/>
  <itemMeta>
    <itemClass qcode="ninat:text"/>
    <provider qcode="nprov:IPTC"/>
    <versionCreated>2020-06-22T12:00:00+03:00</versionCreated>
  </itemMeta>
  <contentSet>
    <inlineXML contenttype="application/nitf+xml"/>
  </contentSet>
</newsItem>
"""
        g2doc = NewsMLG2.NewsMLG2Document(string=test_newsmlg2_string)
        roundtrip_version = bytes(g2doc.to_xml(), 'utf-8')
        assert test_newsmlg2_string == roundtrip_version
        
    def test_roundtrip_from_file(self):
        test_newsmlg2_file = os.path.join('tests', 'test_files', '008_roundtrip_test.xml')
        test_newsml_g2_file_as_bytes = bytes(open(test_newsmlg2_file).read(), 'utf-8')
        g2doc = NewsMLG2.NewsMLG2Document(filename=test_newsmlg2_file)
        roundtrip_version = bytes(g2doc.to_xml(), 'utf-8')
        assert test_newsml_g2_file_as_bytes == roundtrip_version
