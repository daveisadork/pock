import click
import yaml

from pock.api.resources import ResourceManager


resources = ResourceManager()


@click.group(name='resource')
def resource_cli():
    pass


@resource_cli.command(name='list', help='List all resources.')
def resource_list():
    for resource in resources.list():
        print("{name}\t{class}:{provider}:{type}\t{state}".format(**{
            'name': resource.name,
            'class': resource.cls,
            'provider': resource.provider,
            'type': resource.type,
            'state': resource.state,
        }))


@resource_cli.command(name='show', help='Show a resource (in YAML format).')
@click.argument('res_id', metavar='<id>')
def resource_show(res_id):
    resource = resources.get(res_id)
    print(yaml.dump(resource.to_dict(), default_flow_style=False))


@resource_cli.command(name='create', help='Create a new resource.')
@click.argument('res_id', metavar='<id>')
@click.argument('res_type', metavar='<type>')
def resource_create(res_id, res_type):
    cls, provider, _type = res_type.split(':')

    new_resource = resources.create(
        name=res_id,
        cls=cls,
        provider=provider,
        type=_type,
    )

    print("Created resource %s." % new_resource.name)
