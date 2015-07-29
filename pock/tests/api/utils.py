"""Various testing-related utilities.

Hosts functions related to basic emulation of
the CIB, for unit testing purposes.
"""

import os

from pyquery import PyQuery as pq


# Read in CIB, and make a copy that we can revert it to
# between each test.
response_xml = os.path.join(os.path.dirname(__file__), '..', 'fixtures/resources/resources.xml')
with open(response_xml) as cib_f:
    cib = pq(cib_f.read())
    original_cib = cib.clone()


def reset_cib():
    """Resets the testing CIB to the one found in resources.xml."""

    global cib
    cib = original_cib.clone()


def fake_get_cib():
    """Returns the testing CIB."""

    return cib


def fake_update_cib(new_xml, parent='cib'):
    """Updates the testing CIB."""

    cib.find(parent).append(new_xml)
    return cib


def fake_crm_mon():
    """Returns fake output from crm_mon."""

    response = os.path.join(os.path.dirname(__file__), '..', 'fixtures/resources/crm_mon.txt')
    with open(response) as f:
        return f.read()
