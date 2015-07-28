import click

from pock.api.resources import ResourceManager


resources = ResourceManager()


@click.group(name='resource')
def resource_cli():
    pass


@resource_cli.command(name='list')
def resource_list():
    for resource in resources.list():
        print("{name}\t{class}:{provider}:{type}\t{state}".format(**{
            'name': resource.name,
            'class': resource.klass,
            'provider': resource.provider,
            'type': resource.type,
            'state': resource.state,
        }))


@resource_cli.command(name='create')
@click.argument('res_id', metavar='<id>')
@click.argument('res_type', metavar='<type>')
def resource_create(res_id, res_type):
    klass, provider, _type = res_type.split(':')

    new_resource = resources.create(
        name=res_id,
        klass=klass,
        provider=provider,
        type=_type,
    )

    print("Created resource %s." % new_resource.name)
