from email.policy import default
from gpu_exporter.controllers import exporter_controller as controller
import click


@click.command()
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["server", "textfile", "pushgateway"], case_sensitive=False),
    default="server",
    show_default=True,
)
@click.option(
    "--textfile",
    "-tf",
    default="/var/lib/node_exporter/textfile_collector/gpu_exporter.prom",
    show_default=True,
    help="textfile location",
)
@click.option(
    "--port",
    default=9235,
    show_default=True,
    help="default server port",
)
@click.option(
    "--nvidia",
    default=False,
    is_flag=True,
    flag_value=True,
    help="Enable Nvidia metrics",
)
@click.option(
    "--amd", default=False, is_flag=True, flag_value=True, help="Enable AMD metrics"
)
@click.option("--label", "-l", type=(str, str), multiple=True)
def exporter(mode, textfile, port, nvidia, amd, label):
    """Run exporter"""

    controller.start_exporter(
        mode=mode,
        textfile_write_file=textfile,
        server_port=port,
        nvidia_enabled=nvidia,
        amd_enabled=amd,
        custom_labels=label,
    )
