from pyquery import PyQuery as pq

from pock.api import base
from pock.api import utils


class Resource(base.BaseResource):

    fields = [
        'name',
        'klass',
        'provider',
        'type',
        'state',
        'attributes',
        'operations',
    ]

    def __unicode__(self):
        return "<Resource: %s>" % self.name

    @staticmethod
    def from_xml(xml):
        attributes = dict(
            (el.get('name'), el.get('value'))
            for el in pq(xml).find('nvpair'))

        operations = dict(
            (el.get('name'), {
                'interval': el.get('interval'),
                'timeout': el.get('timeout'),
            })
            for el in pq(xml).find('op'))

        return Resource(
            name=xml.get('id'),
            klass=xml.get('class'),
            provider=xml.get('provider'),
            type=xml.get('type'),
            state='',
            attributes=attributes,
            operations=operations,
        )

    def to_dict(self):
        return dict(
            (attr, getattr(self, attr))
            for attr in self.fields)


class ResourceManager(object):
    def list(self):
        xml = utils.cibadmin(['cibadmin', '--query', '--local'])
        return self.from_xml(xml.find('primitive.ocf'))

    def from_xml(self, xml):
        return list(xml.map(lambda _, el: Resource.from_xml(el)))
