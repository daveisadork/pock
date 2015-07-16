

class BaseResource(object):
    name = None

    fields = [
        'id',
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.fields:
                setattr(self, attr, value)

    def __unicode__(self):
        return "<BaseResource: %s>" % self.name

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    @staticmethod
    def from_xml(xml):
        return BaseResource(id=xml.get('id'))
