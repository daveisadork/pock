import os
import unittest

import mock
from pyquery import PyQuery as pq

import pock
from pock.api import utils


__all__ = [
    'ResourceListTests',
]


def fake_utils(command):
    response_xml = os.path.join(os.path.dirname(__file__), '..', 'fixtures/resources.xml')
    with open(response_xml) as f:
        return pq(f.read())


class ResourceListTests(unittest.TestCase):

    def setUp(self):
        self.p = mock.patch.object(utils, 'cibadmin', fake_utils)
        self.p.start()

    def tearDown(self):
        self.p.stop()

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
