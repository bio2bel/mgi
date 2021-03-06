# -*- coding: utf-8 -*-

from typing import Optional

import pandas as pd

from ..constants import ENTREZ_MAPPING_URL

__all__ = [
    'parse_entrez_mapping',
]

column_labels = [
    'MGI Marker Accession ID',
    'Marker Symbol',
    'Status',
    'Marker Name',
    'cM Position',
    'Chromosome',
    'Type',  # One of: Gene, DNA Segment, Other Genome Feature, Complex/Cluster/Region, or microRNA
    'Secondary Accession IDs',
    'Entrez Gene ID',
    'Synonyms',  # pipe delimited
    'Feature Types'  # pipe delimited
    'Genome Coordinate Start',
    'Genome Coordinate End',
    'Strand',
    'BioTypes',  # pipe delimited
]


def parse_entrez_mapping(url: Optional[str] = None) -> pd.DataFrame:
    """Read the MGI to Entrez mapping file.

    :param url: The URL of the Entrez mapping file
    """
    return pd.read_csv(
        url or ENTREZ_MAPPING_URL,
        sep='\t',
        names=column_labels,
    )
