import click

from pock.shell.resource import resource_cli
from pock.shell.cluster import cluster_cli


__all__ = [
    'pock_cli',
]


@click.group(name='pock')
def pock_cli():
    pass


pock_cli.add_command(resource_cli)
pock_cli.add_command(cluster_cli)
