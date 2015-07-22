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
