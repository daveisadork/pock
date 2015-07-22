import unittest

import mock

import pock
from pock.api import utils
from pock.tests.api import utils as test_utils


__all__ = [
    'ResourceListTests',
]


class ResourceListTests(unittest.TestCase):

    def setUp(self):
        self.p1 = mock.patch.object(utils, 'cibadmin', test_utils.fake_cibadmin)
        self.p2 = mock.patch.object(utils, 'crm_mon', test_utils.fake_crm_mon)
        self.p1.start()
        self.p2.start()

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()

    def test_two_resources(self):
        resources = pock.resources.list()

        self.assertEqual(len(resources), 2)

        self.assertEqual(resources[0].name, 'Resource1')
        self.assertEqual(resources[0].attributes, {'foo': 'bar1', 'baz': 'quux1'})
        self.assertEqual(resources[0].operations, {
            'monitor': {'interval': '6', 'timeout': '3'},
            'start': {'interval': '4', 'timeout': '1'},
            'stop': {'interval': '5', 'timeout': '2'}})

        self.assertEqual(resources[1].name, 'Resource2')
        self.assertEqual(resources[1].attributes, {'foo': 'bar2', 'baz': 'quux2'})
        self.assertEqual(resources[1].operations, {
            'monitor': {'interval': '60', 'timeout': '30'},
            'start': {'interval': '40', 'timeout': '10'},
            'stop': {'interval': '50', 'timeout': '20'}})
