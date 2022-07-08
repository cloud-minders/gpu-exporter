from gpu_exporter.config.events_emitter import emitter
import prometheus_client
from gpu_exporter.config.env import (
    pushgateway_username,
    pushgateway_password,
    pushgateway_api_url,
    pushgateway_job_id,
    run_interval_secounds,
)
import time
import toml
from py3nvml import py3nvml as nv
import atexit

from gpu_exporter.collectors import NvidiaCollector, nvidia_collector

pyproject = toml.load("pyproject.toml")["tool"]["poetry"]


def start_exporter(
    mode, textfile_write_file, server_port, nvidia_enabled, amd_enabled, custom_labels
):
    emitter.emit("logger.debug", msg="start_exporter")

    # mode strategies
    def start_server(registry):
        emitter.emit("logger.info", msg=f"Starting metrics server on ::{server_port}")
        print("Under Construction.")

    def run_textfile(registry):
        emitter.emit("logger.info", msg=f"writing metrics to {textfile_write_file}")
        prometheus_client.write_to_textfile(path=textfile_write_file, registry=registry)

    def run_pushgateway(registry):
        emitter.emit("logger.info", msg=f"pushing metrics to {pushgateway_api_url}")

        def pushgateway_auth_handler(url, method, timeout, headers, data):
            return prometheus_client.exposition.basic_auth_handler(
                url,
                method,
                timeout,
                headers,
                data,
                pushgateway_username,
                pushgateway_password,
            )

        job_id = pyproject["name"]
        if pushgateway_job_id != None:
            job_id += f"_{pushgateway_job_id}"

        prometheus_client.push_to_gateway(
            pushgateway_api_url,
            job=job_id,
            registry=registry,
            handler=pushgateway_auth_handler,
        )

    # Add registries
    registry = prometheus_client.CollectorRegistry()

    if nvidia_enabled:
        nv.nvmlInit()
        atexit.register(nv.nvmlShutdown)

        nvidia_collector = NvidiaCollector(nv, custom_labels)
        registry.register(nvidia_collector)

    if amd_enabled:
        pass

    # Start/Run mode strategy
    if mode == "server":
        start_server(registry)
    elif mode == "textfile":
        while True:
            run_textfile(registry)
            time.sleep(run_interval_secounds)
    elif mode == "pushgateway":
        while True:
            run_pushgateway(registry)
            time.sleep(run_interval_secounds)


# if xmrig_url != None:
#     xmrig_collector = XmrigCollector(xmrig_url, custom_labels)
#     registry.register(xmrig_collector)

# if trex_url != None:
#     trex_collector = TrexCollector(trex_url, custom_labels)
#     registry.register(trex_collector)
