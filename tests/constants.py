# -*- coding: utf-8 -*-

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

TEST_ENTREZ_MAPPING_URL = os.path.join(resources_path, 'MGI_EntrezGene.rpt')
TEST_MARKER_URL = os.path.join(resources_path, 'test.MRK_List2.tsv')
