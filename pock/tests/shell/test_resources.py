import os
import unittest

from click.testing import CliRunner
import mock
from pyquery import PyQuery as pq

from pock.shell import pock_cli
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
        p = mock.patch.object(utils, 'cibadmin', fake_utils)
        p.start()
        self.addCleanup(p.stop)

    def test_two_resources(self):
        runner = CliRunner()
        result = runner.invoke(pock_cli, ['resource', 'list'], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, ''.join([
            "Resource1	ocf:test_provider:test_type\n",
            "Resource2	ocf:test_provider:test_type\n"]))
