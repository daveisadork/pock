import os

from pyquery import PyQuery as pq


def fake_cibadmin(_):
    response_xml = os.path.join(os.path.dirname(__file__), '..', 'fixtures/resources.xml')
    with open(response_xml) as f:
        return pq(f.read())


def fake_crm_mon():
    response = os.path.join(os.path.dirname(__file__), '..', 'fixtures/crm_mon.txt')
    with open(response) as f:
        return f.read()
