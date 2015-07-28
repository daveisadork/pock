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
        test_utils.reset_cib()
        self.p1 = mock.patch.object(utils, 'get_cib', test_utils.fake_get_cib)
        self.p2 = mock.patch.object(utils, 'crm_mon', test_utils.fake_crm_mon)
        self.p1.start()
        self.p2.start()

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()

    def test_two_resources(self):
        resources = pock.resources.list()

        self.assertEqual(len(resources), 2)

        self.assertEqual(resources[0].to_dict(), {
            'name': 'Resource1',
            'klass': 'ocf',
            'provider': 'test_provider',
            'type': 'test_type',
            'state': 'Started',
            'attributes': {
                'foo': 'bar1',
                'baz': 'quux1'
            },
            'operations': {
                'monitor': {'interval': '6', 'timeout': '3'},
                'start': {'interval': '4', 'timeout': '1'},
                'stop': {'interval': '5', 'timeout': '2'},
            }
        })

        self.assertEqual(resources[1].to_dict(), {
            'name': 'Resource2',
            'klass': 'ocf',
            'provider': 'test_provider',
            'type': 'test_type',
            'state': 'Stopped',
            'attributes': {
                'foo': 'bar2',
                'baz': 'quux2'
            },
            'operations': {
                'monitor': {'interval': '60', 'timeout': '30'},
                'start': {'interval': '40', 'timeout': '10'},
                'stop': {'interval': '50', 'timeout': '20'},
            }
        })


class ResourceCreateTests(unittest.TestCase):

    def setUp(self):
        test_utils.reset_cib()
        self.p1 = mock.patch.object(utils, 'update_cib', test_utils.fake_update_cib)
        self.p2 = mock.patch.object(utils, 'get_cib', test_utils.fake_get_cib)
        self.p3 = mock.patch.object(utils, 'crm_mon', test_utils.fake_crm_mon)
        self.p1.start()
        self.p2.start()
        self.p3.start()

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()

    def test_resource_create(self):
        resource = pock.resources.create(
            name='TestCreateResource',
            provider='test_provider',
            type='test_type',
            attributes={'foo': 'foo'},
            operations={'start': {
                'timeout': '30',
                'interval': '0',
            }},
        )

        # Make sure that the new Python object got created properly
        self.assertEqual('TestCreateResource', resource.name)
        self.assertEqual('ocf', resource.klass)
        self.assertEqual('test_provider', resource.provider)
        self.assertEqual('test_type', resource.type)

        resources = pock.resources.list()

        self.assertEqual(len(resources), 3)

        self.assertEqual(resources[0].to_dict(), {
            'name': 'Resource1',
            'klass': 'ocf',
            'provider': 'test_provider',
            'type': 'test_type',
            'state': 'Started',
            'attributes': {
                'foo': 'bar1',
                'baz': 'quux1'
            },
            'operations': {
                'monitor': {'interval': '6', 'timeout': '3'},
                'start': {'interval': '4', 'timeout': '1'},
                'stop': {'interval': '5', 'timeout': '2'},
            }
        })

        self.assertEqual(resources[1].to_dict(), {
            'name': 'Resource2',
            'klass': 'ocf',
            'provider': 'test_provider',
            'type': 'test_type',
            'state': 'Stopped',
            'attributes': {
                'foo': 'bar2',
                'baz': 'quux2'
            },
            'operations': {
                'monitor': {'interval': '60', 'timeout': '30'},
                'start': {'interval': '40', 'timeout': '10'},
                'stop': {'interval': '50', 'timeout': '20'},
            }
        })

        self.assertEqual(resources[2].to_dict(), {
            'name': 'TestCreateResource',
            'klass': 'ocf',
            'provider': 'test_provider',
            'type': 'test_type',
            'state': 'Stopped',
            'attributes': {'foo': 'foo'},
            'operations': {'start': {
                'timeout': '30',
                'interval': '0',
            }},
        })
