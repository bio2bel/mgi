# -*- coding: utf-8 -*-

"""This module contains constants for the Bio2BEL MGI package"""

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = 'mgi'
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)

#: This url contains (8) MGI Marker associations to Entrez Gene (tab-delimited)
ENTREZ_MAPPING_URL = 'http://www.informatics.jax.org/downloads/reports/MGI_EntrezGene.rpt'
