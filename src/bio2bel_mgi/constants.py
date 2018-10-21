# -*- coding: utf-8 -*-

"""This module contains constants for the Bio2BEL MGI package."""

import os

from bio2bel.utils import get_data_dir

MODULE_NAME = 'mgi'
DATA_DIR = get_data_dir(MODULE_NAME)

# Markers
MARKERS_URL = 'http://www.informatics.jax.org/downloads/reports/MRK_List2.rpt'
MARKERS_HEADER = [
    'MGI Accession ID',
    'Chr',
    'cM Position',
    'genome coordinate start',
    'genome coordinate end',
    'strand',
    'Marker Symbol',
    'Status',
    'Marker Name',
    'Marker Type',
    'Feature Type',
    'Marker Synonyms (pipe-separated)',
]
MARKERS_PATH = os.path.join(DATA_DIR, 'MRK_List2.rpt')

#: This url contains (8) MGI Marker associations to Entrez Gene (tab-delimited)
ENTREZ_MAPPING_URL = 'http://www.informatics.jax.org/downloads/reports/MGI_EntrezGene.rpt'
ENTREZ_MAPPING_PATH = os.path.join(DATA_DIR, 'MGI_EntrezGene.rpt')
