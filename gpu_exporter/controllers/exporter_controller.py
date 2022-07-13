from gpu_exporter.config.events_emitter import emitter
import prometheus_client
from gpu_exporter.config.env import (
    pushgateway_username,
    pushgateway_password,
    pushgateway_api_url,
    pushgateway_job_id,
    run_interval_secounds,
    server_port as env_server_port,
    textfile_path as env_textfile_path,
)
import time
import toml
from py3nvml import py3nvml as nv
import atexit
from gpu_exporter.collectors import NvidiaCollector
import sys
from http.server import HTTPServer
from os import path

pyproject = toml.load("pyproject.toml")["tool"]["poetry"]


def start_exporter(
    custom_labels=None,
    interval=60,
    push_user=None,
    push_pass=None,
    push_job_id=None,
    push_url="localhost:9091",
    mode="server",
    textfile_path="/var/lib/node_exporter/textfile_collector",
    nvidia_enabled=False,
    amd_enabled=False,
    server_port=9235,
):
    emitter.emit("logger.debug", msg="start_exporter")

    # mode strategies
    def start_server(registry):
        _server_port = env_server_port
        if server_port != 9235 or env_server_port == None:
            _server_port = server_port

        emitter.emit("logger.info", msg=f"Starting metrics server on ::{_server_port}")
        metrics_handler = prometheus_client.MetricsHandler.factory(registry=registry)
        server = HTTPServer(("0.0.0.0", _server_port), metrics_handler)
        server.serve_forever()

    def run_textfile(registry):
        _textfile_path = env_textfile_path
        if (
            textfile_path != "/var/lib/node_exporter/textfile_collector"
            or env_textfile_path == None
        ):
            _textfile_path = textfile_path

        _textfile_path = path.join(_textfile_path, f"{pyproject['name']}.prom")

        emitter.emit("logger.info", msg=f"writing metrics to {_textfile_path}")
        prometheus_client.write_to_textfile(path=_textfile_path, registry=registry)

    def run_pushgateway(registry):
        _pushgateway_api_url = pushgateway_api_url
        if push_url != "localhost:9091" or pushgateway_api_url == None:
            _pushgateway_api_url = push_url

        _pushgateway_username = pushgateway_username
        if push_user != None:
            _pushgateway_username = push_user

        _pushgateway_password = pushgateway_password
        if push_pass != None:
            _pushgateway_password = push_pass

        _pushgateway_job_id = pushgateway_job_id
        if push_job_id != None:
            _pushgateway_job_id = push_job_id

        emitter.emit("logger.info", msg=f"pushing metrics to {_pushgateway_api_url}")

        def pushgateway_auth_handler(url, method, timeout, headers, data):
            return prometheus_client.exposition.basic_auth_handler(
                url,
                method,
                timeout,
                headers,
                data,
                _pushgateway_username,
                _pushgateway_password,
            )

        job_id = pyproject["name"]
        if _pushgateway_job_id != None:
            job_id += f"_{_pushgateway_job_id}"

        prometheus_client.push_to_gateway(
            _pushgateway_api_url,
            job=job_id,
            registry=registry,
            handler=pushgateway_auth_handler,
        )

    # Add registries
    registry = prometheus_client.CollectorRegistry()

    if nvidia_enabled != None:
        nv.nvmlInit()
        atexit.register(nv.nvmlShutdown)

        nvidia_collector = NvidiaCollector(nv, custom_labels)
        registry.register(nvidia_collector)

    if amd_enabled != None:
        pass

    # Start/Run mode strategy
    _run_interval_secounds = run_interval_secounds
    if interval != 60 or run_interval_secounds == None:
        _run_interval_secounds = interval

    if mode == "server":
        start_server(registry)
    elif mode == "textfile":
        while True:
            run_textfile(registry)
            time.sleep(_run_interval_secounds)
    elif mode == "pushgateway":
        while True:
            run_pushgateway(registry)
            time.sleep(_run_interval_secounds)
    elif mode == "stdout":
        sys.stdout.write(prometheus_client.generate_latest(registry).decode("utf-8"))
