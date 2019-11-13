# -*- coding: utf-8 -*-

"""Manager for Bio2BEL MGI."""

import logging
from typing import Iterable, Mapping, Optional, Tuple, List

import networkx as nx
from tqdm import tqdm

from bio2bel.manager import AbstractManager
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from pybel import BELGraph
from pybel.constants import IDENTIFIER, NAME, NAMESPACE
from pybel.dsl import BaseEntity
from pybel.manager.models import Namespace, NamespaceEntry
from .constants import MODULE_NAME
from .models import Base, MouseGene
from .parsers import get_marker_df

__all__ = [
    'Manager',
]

logger = logging.getLogger(__name__)


class Manager(AbstractManager, BELNamespaceManagerMixin, FlaskMixin):
    """Mouse genome nomenclature."""

    _base = Base
    module_name = MODULE_NAME

    flask_admin_models = [MouseGene]

    namespace_model = MouseGene
    identifiers_recommended = 'Mouse Genome Database'
    identifiers_pattern = r'^MGI:\d+$'
    identifiers_miriam = 'MIR:00000037'
    identifiers_namespace = 'mgi'
    identifiers_url = 'http://identifiers.org/mgi/'

    def count_mouse_genes(self) -> int:
        """Count the number of genes in the database."""
        return self._count_model(MouseGene)

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database."""
        return dict(mouse_genes=self.count_mouse_genes())

    def is_populated(self) -> bool:
        """Check if the database is populated."""
        return 0 < self.count_mouse_genes()

    def populate(self, marker_url: Optional[str] = None):
        """Populate the database."""
        marker_df = get_marker_df(url=marker_url)
        marker_df.to_sql(MouseGene.__tablename__, self.engine, if_exists='append', index=False)
        self.session.commit()

    def get_genes(self) -> List[MouseGene]:
        """Get all mouse genes."""
        return self._get_query(MouseGene).all()

    def get_gene_by_mgi_id(self, mgi_id: str) -> Optional[MouseGene]:
        """Get a gene by its MGI gene identifier, if it exists.

        :param mgi_id: An MGI gene identifier (automatically strips the "MGI:" prefix if present)
        """
        return self._get_query(MouseGene).filter(MouseGene.mgi_id == mgi_id).one_or_none()

    def get_gene_by_mgi_symbol(self, mgi_symbol: str) -> Optional[MouseGene]:
        """Get a gene by its MGI gene symbol, if it exists.

        :param mgi_symbol: An MGI gene symbol
        """
        return self._get_query(MouseGene).filter(MouseGene.symbol == mgi_symbol).one_or_none()

    def get_gene_by_entrez_id(self, entrez_id: str) -> Optional[MouseGene]:
        """Get a gene by its Entrez gene identifier, if it exists.

        :param entrez_id: An Entrez gene identifier
        """
        raise NotImplementedError

    def enrich_entrez_equivalences(self, graph: BELGraph):
        """Add equivalent Entrez nodes for MGI nodes."""
        raise NotImplementedError

    def normalize_mouse_genes(self, graph: BELGraph, use_tqdm: bool = False) -> None:
        mapping = {
            node: gene_model.as_bel(func=node.function)
            for node, gene_model in self.iter_mouse_genes(graph, use_tqdm=use_tqdm)
        }
        nx.relabel_nodes(graph, mapping, copy=False)

    def iter_mouse_genes(self, graph: BELGraph, use_tqdm: bool = False) -> Iterable[Tuple[BaseEntity, MouseGene]]:
        """Iterate over pairs of BEL nodes and MGI genes."""
        it = (
            tqdm(graph, desc='Mouse genes')
            if use_tqdm else
            graph
        )
        for node in it:
            rat_gene = self.get_mouse_gene_from_bel(node)
            if rat_gene is not None:
                yield node, rat_gene

    def get_mouse_gene_from_bel(self, node: BaseEntity) -> Optional[MouseGene]:
        namespace = node.get(NAMESPACE)

        if not namespace or namespace.lower() not in {'mgi', 'mgiid'}:
            return

        identifier = node.get(IDENTIFIER)
        name = node.get(NAME)

        if identifier is None and name is None:
            raise ValueError

        if namespace.lower() == 'mgiid':
            return self.get_gene_by_mgi_id(name)

        elif namespace.lower() == 'mgi':
            if identifier is not None:
                return self.get_gene_by_mgi_id(identifier)
            else:  # elif name is not None:
                return self.get_gene_by_mgi_symbol(name)

        logger.warning('Could not map MGI node: %r', node)

    @staticmethod
    def _get_identifier(mouse_gene: MouseGene) -> str:
        return mouse_gene.mgi_id

    @staticmethod
    def _get_name(mouse_gene: MouseGene) -> str:
        return mouse_gene.symbol

    def _create_namespace_entry_from_model(self, mouse_gene: MouseGene, namespace: Namespace) -> NamespaceEntry:
        return NamespaceEntry(
            encoding=mouse_gene.bel_encoding,
            name=mouse_gene.symbol,
            identifier=mouse_gene.mgi_id,
            namespace=namespace,
        )

    def build_mgi_gene_symbol_to_mgi_id_mapping(self) -> Mapping[str, str]:
        """Build a mapping from MGI symbols to their MGI identifiers."""
        return dict(self.session.query(MouseGene.symbol, MouseGene.mgi_id).all())
