from jinja2 import Template
from pyquery import PyQuery as pq

from pock.api import exceptions
from pock.api import utils


class Resource(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.cls = kwargs.get('cls')
        self.provider = kwargs.get('provider')
        self.type = kwargs.get('type')
        self.state = kwargs.get('state')
        self.attributes = kwargs.get('attributes')
        self.operations = kwargs.get('operations')

    def __unicode__(self):
        return "<Resource: %s>" % self.name

    @staticmethod
    def from_xml(xml):
        """Creates a Resource from a cibadmin XML string.

        :param xml: The XML to parse
        """

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
            cls=xml.get('class'),
            provider=xml.get('provider'),
            type=xml.get('type'),
            state=state,
            attributes=attributes,
            operations=operations)

    def to_xml(self):
        template = Template("""
            <primitive class="{{ class }}" id="{{ name }}" provider="{{ provider }}" type="{{ type }}">
              <instance_attributes id="{{ name }}-instance_attributes">
                {% for key, value in attributes.items() %}
                <nvpair id="{{ name }}-instance_attributes-{{ key }}" name="{{ key }}" value="{{ value }}"/>
                {% endfor %}
              </instance_attributes>
              <operations>
                {% for key, value in operations.items() %}
                <op id="{{ name }}-{{ key }}-timeout-{{ value.interval }}" interval="{{ value.interval }}"
                  name="{{ key }}" timeout="{{ value.timeout }}"/>
                {% endfor %}
              </operations>
            </primitive>
        """)

        return pq(template.render(**{
            'class': self.cls,
            'name': self.name,
            'provider': self.provider,
            'type': self.type,
            'attributes': self.attributes,
            'operations': self.operations,
        }))

    def to_dict(self):
        return {
            'name': self.name,
            'cls': self.cls,
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

    def get(self, res_id):
        try:
            return next(r for r in self.list() if r.name == res_id)
        except StopIteration:
            raise exceptions.ResourceNotFound('The resource "%s" could not be found.' % res_id)

    def create(self, **kwargs):
        new_resource = Resource(
            name=kwargs['name'],
            cls=kwargs.get('cls', 'ocf'),
            provider=kwargs['provider'],
            type=kwargs['type'],
            state=kwargs.get('state', 'Stopped'),
            attributes=kwargs.get('attributes', {}),
            operations=kwargs.get('operations', {}))

        utils.update_cib(new_resource.to_xml(), parent='resources')

        return new_resource

    def from_xml(self, xml):
        return list(xml.map(lambda _, el: Resource.from_xml(el)))
