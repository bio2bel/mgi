# -*- coding: utf-8 -*-

from bio2bel.testing import AbstractTemporaryCacheClassMixin

from bio2bel_mgi import Manager
from .constants import TEST_MARKER_URL


class TemporaryCacheClassMixin(AbstractTemporaryCacheClassMixin):
    Manager = Manager

    @classmethod
    def populate(cls):
        cls.manager.populate(
            marker_url=TEST_MARKER_URL,
        )
