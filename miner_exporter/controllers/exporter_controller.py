from miner_exporter.config.events_emitter import emitter
import prometheus_client
from miner_exporter.collectors import XmrigCollector, TrexCollector
from miner_exporter.config.env import (
    pushgateway_username,
    pushgateway_password,
    push_interval_secounds,
    pushgateway_api_url,
    pushgateway_job_id,
)
import time
import toml

pyproject = toml.load("pyproject.toml")["tool"]["poetry"]


def start_exporter(xmrig_url, trex_url, custom_labels):
    emitter.emit("logger.debug", msg="start_exporter")

    # todo: add logic that let's the collectors continuously ping the API they pull data from without crashing if it's not there, or still spinning up. Then we can remove this arbitrary wait time.
    # Wait an arbitrary amount of time for miners to start before metrics
    time.sleep(60)

    registry = prometheus_client.CollectorRegistry()

    if xmrig_url != None:
        xmrig_collector = XmrigCollector(xmrig_url, custom_labels)
        registry.register(xmrig_collector)

    if trex_url != None:
        trex_collector = TrexCollector(trex_url, custom_labels)
        registry.register(trex_collector)

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

    # post to pushgateway every push_interval_secounds
    while True:
        emitter.emit("logger.info", msg=f"pushing metrics to {pushgateway_api_url}")

        job_id = pyproject["name"]
        if pushgateway_job_id != None:
            job_id += f"_{pushgateway_job_id}"

        prometheus_client.push_to_gateway(
            pushgateway_api_url,
            job=job_id,
            registry=registry,
            handler=pushgateway_auth_handler,
        )
        time.sleep(push_interval_secounds)
