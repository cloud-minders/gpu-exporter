import click
import toml
from gpu_exporter.cli.exporter_command import exporter

pyproject = toml.load("pyproject.toml")["tool"]["poetry"]


@click.group()
@click.version_option(version=pyproject["version"], prog_name=pyproject["name"])
def cli():
    pass


cli.add_command(exporter)
