import unittest

from click.testing import CliRunner
import mock

from pock.api import utils
from pock.shell import pock_cli
from pock.tests.api import utils as test_utils


__all__ = [
    'ResourceListTests',
]


class ResourceListTests(unittest.TestCase):

    def setUp(self):
        self.p1 = mock.patch.object(utils, 'get_cib', test_utils.fake_get_cib)
        self.p2 = mock.patch.object(utils, 'crm_mon', test_utils.fake_crm_mon)
        self.p1.start()
        self.p2.start()

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()

    def test_two_resources(self):
        runner = CliRunner()
        result = runner.invoke(pock_cli, ['resource', 'list'], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, ''.join([
            "Resource1\tocf:test_provider:test_type\tStarted\n",
            "Resource2\tocf:test_provider:test_type\tStopped\n"]))
