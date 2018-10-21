# -*- coding: utf-8 -*-

from typing import Mapping, Optional

from bio2bel.manager import AbstractManager
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from pybel import BELGraph
from pybel.manager.models import Namespace, NamespaceEntry
from .constants import MODULE_NAME
from .models import Base, Gene
from .parsers import get_marker_df


class Manager(AbstractManager, BELNamespaceManagerMixin, FlaskMixin):
    """Manages the MGI database."""

    @staticmethod
    def _get_identifier(model: Gene):
        return model.mgi_id

    def _create_namespace_entry_from_model(self, model: Gene, namespace: Namespace) -> NamespaceEntry:
        return NamespaceEntry(
            name=model.name,
            identifier=model.mgi_id,
            namespace=namespace,
        )

    _base = Base
    module_name = MODULE_NAME
    flask_admin_models = [Gene]
    namespace_model = Gene

    def count_genes(self) -> int:
        """Count the number of genes in the database."""
        return self._count_model(Gene)

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database."""
        return dict(genes=self.count_genes())

    def is_populated(self) -> bool:
        """Check if the database is populated."""
        return 0 < self.count_genes()

    def populate(self, marker_url: Optional[str] = None):
        """Populate the database."""
        marker_df = get_marker_df(url=marker_url)
        marker_df.to_sql(Gene.__tablename__, self.engine, if_exists='append', index=False)
        self.session.commit()

    def get_gene_by_mgi_id(self, mgi_id: str) -> Optional[Gene]:
        """Get a gene by its MGI gene identifier, if it exists.

        :param mgi_id: An MGI gene identifier (automatically strips the "MGI:" prefix if present)
        """
        return self._get_query(Gene).filter(Gene.mgi_id == mgi_id).one_or_none()

    def get_gene_by_mgi_symbol(self, mgi_symbol: str) -> Optional[Gene]:
        """Get a gene by its MGI gene symbol, if it exists.

        :param mgi_symbol: An MGI gene symbol
        """
        return self._get_query(Gene).filter(Gene.symbol == mgi_symbol).one_or_none()

    def get_gene_by_entrez_id(self, entrez_id: str) -> Optional[Gene]:
        """Get a gene by its Entrez gene identifier, if it exists.

        :param entrez_id: An Entrez gene identifier
        """
        raise NotImplementedError

    def enrich_entrez_equivalences(self, graph: BELGraph):
        """Add equivalent Entrez nodes for MGI nodes."""
        raise NotImplementedError
