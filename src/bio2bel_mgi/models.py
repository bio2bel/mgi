# -*- coding: utf-8 -*-

"""MGI database models."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import pybel.dsl
from .constants import MODULE_NAME

Base = declarative_base()

GENE_TABLE_NAME = f'{MODULE_NAME}_gene'


class Gene(Base):  # type: ignore
    """Gene table."""

    __tablename__ = GENE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    mgi_id = Column(String(255), nullable=False, index=True, doc='KEGG id of the protein')
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

    def __repr__(self):
        """Return HGNC symbol."""
        return str(self.mgi_id)

    def __str__(self):
        """Return HGNC symbol."""
        return str(self.mgi_id)

    def serialize_to_protein_node(self) -> pybel.dsl.Gene:
        """Serialize to PyBEL node data dictionary."""
        return pybel.dsl.Gene(
            namespace='mgi',
            name=self.symbol,
            identifier=str(self.mgi_id)
        )
