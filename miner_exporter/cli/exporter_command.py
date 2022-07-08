from miner_exporter.controllers import exporter_controller as controller
import click


@click.command()
@click.option("--xmrig-url", help="The xmrig API address")
@click.option("--trex-url", help="The t-rex API address")
@click.option("--label", "-l", type=(str, str), multiple=True)
def exporter(xmrig_url, trex_url, label):
    """Run exporter"""
    controller.start_exporter(
        trex_url=trex_url, xmrig_url=xmrig_url, custom_labels=label
    )
