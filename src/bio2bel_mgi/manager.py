# -*- coding: utf-8 -*-


class Manager(object):
    """Manages the MGI database"""

    def __init__(self, connection=None):
        """

        :param Optional[str] connection:
        """
        raise NotImplementedError

    def drop_all(self):
        """Drops the database"""
        raise NotImplementedError

    def create_all(self):
        """Creates the database"""
        raise NotImplementedError

    def populate(self):
        """Populates the database"""
        raise NotImplementedError

    def get_gene_by_mgi_id(self, mgi_id):
        """Gets a gene by its MGI gene identifier if it exists

        :param str mgi_id: An MGI gene identifier (automatically strips the "MGI:" prefix if present)
        :rtype: Optional[Gene]
        """
        raise NotImplementedError

    def get_gene_by_mgi_symbol(self, mgi_symbol):
        """Gets a gene by its MGI gene symbol if it exists

        :param str mgi_symbol: An MGI gene symbol
        :rtype: Optional[Gene]
        """
        raise NotImplementedError

    def get_gene_by_entrez_id(self, entrez_id):
        """Gets a gene by its Entrez gene identifier if it exists

        :param str entrez_id: An Entrez gene identifier
        :rtype: Optional[Gene]
        """
        raise NotImplementedError

    def enrich_entrez_equivalences(self, graph):
        """Adds equivalent Entrez nodes for MGI nodes

        :type graph: pybel.BELGraph
        """
        raise NotImplementedError
