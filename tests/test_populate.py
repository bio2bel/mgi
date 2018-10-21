# -*- coding: utf-8 -*-

from bio2bel_mgi import Manager
from tests.cases import TemporaryCacheClassMixin


class TestPopulate(TemporaryCacheClassMixin):
    """"""

    manager: Manager

    def test_count(self):
        self.assertEqual(9, self.manager.count_mouse_genes())
