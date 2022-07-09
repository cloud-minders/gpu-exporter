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
    "-p",
    default=9235,
    show_default=True,
    help="server port",
)
@click.option(
    "--push-url",
    "-pu",
    default="localhost:9091",
    show_default=True,
    help="pushgateway url",
)
@click.option(
    "--push-user",
    help="pushgateway username",
)
@click.option(
    "--push-pass",
    help="pushgateway password",
)
@click.option(
    "--push-job-id",
    help="pushgateway suffix for job name",
)
@click.option(
    "--interval",
    "-i",
    default=60,
    help="Interval in seconds for scraping metrics",
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
def exporter(
    mode,
    textfile,
    port,
    push_url,
    push_user,
    push_pass,
    push_job_id,
    interval,
    nvidia,
    amd,
    label,
):
    """Run exporter"""

    controller.start_exporter(
        interval=interval,
        push_user=push_user,
        push_pass=push_pass,
        push_url=push_url,
        push_job_id=push_job_id,
        mode=mode,
        textfile_write_file=textfile,
        server_port=port,
        nvidia_enabled=nvidia,
        amd_enabled=amd,
        custom_labels=label,
    )
