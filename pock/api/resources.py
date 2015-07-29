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
        """Creates a Resource from a cibadmin XML string."""

        res_id = xml.get('id')
        state = utils.get_state(res_id)

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
            name=res_id,
            klass=xml.get('class'),
            provider=xml.get('provider'),
            type=xml.get('type'),
            state=state,
            attributes=attributes,
            operations=operations)

    def to_xml(self):
        template = """
            <primitive class="{class}" id="{name}" provider="{provider}" type="{type}">
              <instance_attributes id="{name}-instance_attributes">
                {attributes}
              </instance_attributes>
              <operations>
                {operations}
              </operations>
            </primitive>
        """

        nvpair_template = '<nvpair id="{name}-instance_attributes-{key}" ' \
                          'name="{key}" value="{value}"/>'
        op_template = '<op id="{name}-{key}-timeout-{interval}" interval="{interval}" ' \
                      'name="{key}" timeout="{timeout}"/>'

        return pq(template.format(**{
            'class': self.klass,
            'name': self.name,
            'provider': self.provider,
            'type': self.type,
            'attributes': '\n'.join(
                nvpair_template.format(**{
                    'name': self.name,
                    'key': key,
                    'value': value,
                })
                for key, value in self.attributes.items()),
            'operations': '\n'.join(
                op_template.format(**{
                    'name': self.name,
                    'key': key,
                    'timeout': value['timeout'],
                    'interval': value['interval'],
                })
                for key, value in self.operations.items()),
        }))

    def to_dict(self):
        return {
            'name': self.name,
            'klass': self.klass,
            'provider': self.provider,
            'type': self.type,
            'state': self.state,
            'attributes': self.attributes,
            'operations': self.operations,
        }


class ResourceManager(object):
    def list(self):
        xml = utils.get_cib()
        return self.from_xml(xml.find('primitive.ocf'))

    def create(self, **kwargs):
        new_resource = Resource(
            name=kwargs['name'],
            klass=kwargs.get('klass', 'ocf'),
            provider=kwargs['provider'],
            type=kwargs['type'],
            state=kwargs.get('state', 'Stopped'),
            attributes=kwargs.get('attributes', {}),
            operations=kwargs.get('operations', {}))

        utils.update_cib(new_resource.to_xml(), parent='resources')

        return new_resource

    def from_xml(self, xml):
        return list(xml.map(lambda _, el: Resource.from_xml(el)))
