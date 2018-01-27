# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

from bio2bel_mgi import Manager

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

test_entrez_mapping = os.path.join(resources_path, 'MGI_EntrezGene.rpt')


class DatabaseMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary file"""

        cls.fd, cls.path = tempfile.mkstemp()
        cls.connection = 'sqlite:///' + cls.path

        # create temporary database
        cls.manager = Manager(connection=cls.connection)

        # fill temporary database with test data
        cls.manager.populate(

        )

    @classmethod
    def tearDownClass(cls):
        """Closes the connection in the manager and deletes the temporary database"""
        cls.manager.session.close()
        os.close(cls.fd)
        os.remove(cls.path)
