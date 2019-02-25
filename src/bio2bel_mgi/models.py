# -*- coding: utf-8 -*-

"""MGI database models."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import pybel.dsl
from .constants import MODULE_NAME

Base = declarative_base()

MOUSE_GENE_TABLE_NAME = f'{MODULE_NAME}_mouseGene'

marker_type_to_encoding = {
    'BAC/YAC end': 'G',
    'DNA Segment': 'G',
    'Gene': 'G',
    'Pseudogene': 'G',
    'Other Genome Feature': 'G',
    'QTL': 'G',
    'Complex/Cluster/Region': 'G',
    'Cytogenetic Marker': 'G',
    'Transgene': 'G',
}

feature_type_to_encoding = {
    'antisense lncRNA gene': 'GR',
    'lincRNA gene': 'GR',
    'unclassified gene': 'G',
    'protein coding gene': 'GRP',
    'unclassified non-coding RNA gene': 'GR',
    'lncRNA gene': 'GR',
    'sense intronic lncRNA gene': 'GR',
    'heritable phenotypic marker': 'GR',
    'bidirectional promoter lncRNA gene': 'GR',
    'sense overlapping lncRNA gene': 'GR',
    'snoRNA gene': 'GR',
    'non-coding RNA gene': 'GR',
    'gene': 'G',
    'gene segment': 'G',
    'miRNA gene': 'GM',
    'snRNA gene': 'GR',
    'rRNA gene': 'GR',
    'ribozyme gene': 'GRP',
    'tRNA gene': 'GR',
    'RNase MRP RNA gene': 'GR',
    'SRP RNA gene': 'GR',
    'scRNA gene': 'GR',
    'RNase P RNA gene': 'GR',
    'telomerase RNA gene': 'GR',
}


class MouseGene(Base):  # type: ignore
    """Gene table."""

    __tablename__ = MOUSE_GENE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    mgi_id = Column(String(255), nullable=False, index=True)
    # chromosome = ...
    # position = ...
    # start
    # end = ...
    # strand = ...
    symbol = Column(String(255), nullable=False, index=True)
    # status = ...
    name = Column(String(255), nullable=False, index=True)
    marker_type = Column(String(255), nullable=False, index=True)
    feature_type = Column(String(255), nullable=False, index=True)

    # synonyms = list!

    @property
    def bel_encoding(self):
        if self.marker_type == 'Gene':
            return feature_type_to_encoding[self.feature_type]
        return marker_type_to_encoding[self.marker_type]

    def __repr__(self):
        """Return HGNC symbol."""
        return str(self.mgi_id)

    def __str__(self):
        """Return HGNC symbol."""
        return str(self.mgi_id)

    def as_bel(self, func=None) -> pybel.dsl.CentralDogma:
        """Make a PyBEL DSL object from this gene."""
        dsl = pybel.dsl.Gene if func is None else pybel.dsl.FUNC_TO_DSL[func]
        return dsl(
            namespace=MODULE_NAME,
            name=str(self.symbol),
            identifier=str(self.mgi_id),
        )
