#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
NewsML-G2 Python library - check that every test file is valid against the
NewsML-G2 schema, so the other tests are run against real NewsML-G2

"""

import glob
import os
import unittest

from lxml import etree

DIRNAME = os.path.dirname(os.path.realpath(__file__))
SCHEMA_FILE = os.path.join(
    DIRNAME, 'schema', 'NewsML-G2_2.36-spec-All-Power.xsd'
)
TEST_FILES = sorted(glob.glob(os.path.join(DIRNAME, 'test_files', '*.xml')))


class TestNewsMLG2TestFilesAreValid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema = etree.XMLSchema(etree.parse(SCHEMA_FILE))

    def test_test_files_exist(self):
        assert len(TEST_FILES) > 0

    def test_test_files_validate(self):
        for filename in TEST_FILES:
            with self.subTest(file=os.path.basename(filename)):
                if not self.schema.validate(etree.parse(filename)):
                    self.fail('\n'.join(
                        str(error) for error in self.schema.error_log
                    ))


if __name__ == '__main__':
    unittest.main()
