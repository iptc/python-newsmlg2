#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Copyright (c) 2026, IPTC
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
NewsML-G2 Python library - unit tests for features added in NewsML-G2 2.36

"""

import os
import sys
import unittest
sys.path.append(os.getcwd())

import NewsMLG2

DIRNAME = os.path.dirname(os.path.realpath(__file__))
TEST_FILE = os.path.join(
    DIRNAME, 'test_files', '009_newsitem_2.36_features.xml'
)


class TestNewsMLG2v236Features(unittest.TestCase):

    def setUp(self):
        self.newsitem = NewsMLG2.NewsMLG2Document(TEST_FILE).get_item()

    def test_standardversion(self):
        assert self.newsitem.standardversion == '2.36'
        assert NewsMLG2.NEWSMLG2_VERSION == '2.36'

    def test_aiinfo(self):
        aiinfo = self.newsitem.contentmeta.aiinfo[0]
        assert type(aiinfo) == NewsMLG2.contentmeta.AIInfo
        assert aiinfo.id == 'ai1'

        system = aiinfo.system
        assert system.qcode == 'aisys:examplemodel'
        assert system.versioninfo == '4.2'
        assert str(system.name) == 'Example Model'
        assert system.provider.qcode == 'nprov:ExampleAI'

        assert str(aiinfo.promptinfo) == (
            'Summarise the attached press release in 200 words.'
        )
        assert aiinfo.promptinfo.xml_lang == 'en'

        assert aiinfo.promptwriter.qcode == 'staff:jdoe'
        assert str(aiinfo.promptwriter.name) == 'Jo Doe'

    def test_hop_action_refs(self):
        action = self.newsitem.hophistory.hop[0].action[0]
        assert action.targetrefs == 'hl1'
        assert action.detailrefs == 'ai1'

    def test_altloc_roleuri(self):
        altloc = self.newsitem.contentset.remotecontent[0].altloc[0]
        assert altloc.role == 'locrole:backup'
        assert altloc.roleuri == 'http://example.com/roles/backup'

    def test_altloc_legacy_roleruri(self):
        """
        Documents written against 2.18-2.35 may use the misspelled "roleruri"
        attribute; make sure they still parse.
        """
        g2doc = NewsMLG2.NewsMLG2Document(b"""<?xml version="1.0" encoding="UTF-8"?>
<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/" guid="legacy" standard="NewsML-G2" standardversion="2.35" conformance="power" version="1">
  <itemMeta>
    <itemClass qcode="ninat:text"/>
    <provider qcode="nprov:IPTC"/>
    <versionCreated>2025-01-01T00:00:00Z</versionCreated>
  </itemMeta>
  <contentSet>
    <remoteContent href="http://example.com/a.html">
      <altLoc roleruri="http://example.com/roles/backup">http://mirror.example.com/a.html</altLoc>
    </remoteContent>
  </contentSet>
</newsItem>
""")
        altloc = g2doc.get_item().contentset.remotecontent[0].altloc[0]
        assert altloc.roleruri == 'http://example.com/roles/backup'

    def test_exclaudience_and_altid(self):
        contentmeta = self.newsitem.contentmeta
        assert contentmeta.exclaudience[0].qcode == 'exclaud:minors'
        assert str(contentmeta.altid[0]) == 'alt-1'

    def test_aiinfo_roundtrip(self):
        xml = NewsMLG2.NewsMLG2Document(TEST_FILE).to_xml_string()
        assert '<aiInfo id="ai1">' in xml
        assert '<system qcode="aisys:examplemodel" versioninfo="4.2">' in xml
        assert '<promptInfo xml:lang="en">' in xml
        assert 'targetrefs="hl1"' in xml
        assert 'roleuri="http://example.com/roles/backup"' in xml


if __name__ == '__main__':
    unittest.main()
