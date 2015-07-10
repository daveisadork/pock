import click


@click.group(name='resource')
def resource_cli():
    pass

@resource_cli.command(name='show')
def resource_show():
    print("Showing resources!")
