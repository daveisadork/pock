import click


@click.group(name='cluster')
def cluster_cli():
    pass

@cluster_cli.command(name='show')
def cluster_show():
    print("Showing clusters!")
