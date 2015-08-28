import sys

import click

from pock.shell.resource import resource_cli
from pock.shell.cluster import cluster_cli


__all__ = [
    'pock_cli',
]


def exception_handler(exc_type, exc, _):
    """Prints only the error message and not the stack trace.

    Used by default, can be turned off by passing the
    `--verbose` flag.
    """

    print("%s: %s" % (exc_type.__name__, exc))


@click.group(name='pock')
@click.option('--verbose', is_flag=True)
def pock_cli(verbose):
    if not verbose:
        sys.excepthook = exception_handler


pock_cli.add_command(resource_cli)
pock_cli.add_command(cluster_cli)
