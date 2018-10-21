# -*- coding: utf-8 -*-

from bio2bel_mgi import Manager
from tests.cases import TemporaryCacheClassMixin


class TestPopulate(TemporaryCacheClassMixin):
    """"""

    manager: Manager

    def test_count(self):
        self.assertEqual(10, self.manager.count_genes())
