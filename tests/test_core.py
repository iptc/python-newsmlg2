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
NewsML-G2 Python library - core library unit tests

"""

from lxml import etree
import os
import sys
import unittest
sys.path.append(os.getcwd())

import NewsMLG2

class TestNewsMLG2NewsItemStrings(unittest.TestCase):

    def test_bad_xml_element(self):
        with self.assertRaises(AttributeError):
            g2doc = NewsMLG2.NewsItem(xmlelement="foo")

    def test_genericarray_with_no_elementclass(self):
        with self.assertRaises(AttributeError):
            g2doc = NewsMLG2.GenericArray(xmlarray=[])

    def test_non_xml_root_element(self):
        with self.assertRaises(Exception):
            g2doc = NewsMLG2.NewsMLG2Document(string='<foo></foo>')

if __name__ == '__main__':
    unittest.main()
