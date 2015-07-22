import unittest

import mock

from pock.api import utils
from pock.tests.api import utils as test_utils


__all__ = [
    'UtilsTests',
]


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.p = mock.patch.object(utils, 'crm_mon', test_utils.fake_crm_mon)
        self.p.start()

    def tearDown(self):
        self.p.stop()

    def test_get_state(self):
        # Existing resources
        self.assertEqual('Started', utils.get_state('Resource1'))
        self.assertEqual('Stopped', utils.get_state('Resource2'))
        self.assertEqual('Started', utils.get_state('Resource3'))
        self.assertEqual('Stopped', utils.get_state('Resource4'))

        # Non-existent resources
        self.assertEqual(None, utils.get_state('Resource0'))
        self.assertEqual(None, utils.get_state('Resource5'))
