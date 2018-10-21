# -*- coding: utf-8 -*-

"""Tests the MGI parsers"""

import unittest

from bio2bel_mgi.parsers.entrez_mapping import column_labels, parse_entrez_mapping
from tests.constants import TEST_ENTREZ_MAPPING_URL


class TestEntrezMapping(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Parses the test Entrez mapping file"""
        cls.df = parse_entrez_mapping(url=TEST_ENTREZ_MAPPING_URL)

    def test_exists(self):
        self.assertIsNotNone(self.df)

    def test_count_columns(self):
        self.assertEqual(column_labels, list(self.df.columns))

    def test_has_id(self):
        self.assertIn('MGI:87861', self.df['MGI Marker Accession ID'])
        self.assertNotIn('MGI:87872', self.df['MGI Marker Accession ID'],
                         msg='This entry should not be included in the test data')
