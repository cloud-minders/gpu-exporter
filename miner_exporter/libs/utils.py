from prometheus_client.core import (
    CounterMetricFamily,
    GaugeMetricFamily,
    InfoMetricFamily,
)
import base64
from typing import Callable, List, Optional, Sequence, Tuple
import requests


def _make_handler(
    url: str,
    method: str,
    timeout: Optional[float],
    _headers: Sequence[Tuple[str, str]],
    data: bytes,
) -> Callable[[], None]:
    def handle() -> None:
        headers = {}

        for k, v in _headers:
            headers[k] = v

        resp = requests.request(
            method=method, url=url, data=data.decode(), headers=headers, timeout=timeout
        )

        if resp.status_code >= 400:
            raise OSError(
                f"error talking to pushgateway: {resp.status_code} {resp.text}"
            )

    return handle


def default_handler(
    url: str,
    method: str,
    timeout: Optional[float],
    headers: List[Tuple[str, str]],
    data: bytes,
) -> Callable[[], None]:
    """Default handler that implements HTTP/HTTPS connections.

    Used by the push_to_gateway functions. Can be re-used by other handlers."""

    return _make_handler(url, method, timeout, headers, data)


def basic_auth_handler(
    url: str,
    method: str,
    timeout: Optional[float],
    headers: List[Tuple[str, str]],
    data: bytes,
    username: str = None,
    password: str = None,
) -> Callable[[], None]:
    """Handler that implements HTTP/HTTPS connections with Basic Auth.

    Sets auth headers using supplied 'username' and 'password', if set.
    Used by the push_to_gateway functions. Can be re-used by other handlers."""

    def handle():
        """Handler that implements HTTP Basic Auth."""
        if username is not None and password is not None:
            auth_value = f"{username}:{password}".encode()
            auth_token = base64.b64encode(auth_value)
            auth_header = b"Basic " + auth_token
            headers.append(("Authorization", auth_header.decode()))
        default_handler(url, method, timeout, headers, data)()

    return handle


def make_metric(name, documentation, value, metric_type="counter", **labels):
    """
    It takes a metric name, documentation, value, and a dictionary of labels, and returns a metric
    object

    :param name: The name of the metric
    :param documentation: A string that will be used as the documentation for the metric
    :param value: The value of the metric
    :param metric_type: The type of metric. Can be one of: counter, gauge, summary, histogram, defaults
    to counter (optional)
    :return: A metric object
    """
    label_names = list(labels.keys())

    c = CounterMetricFamily

    if metric_type == "gauge":
        c = GaugeMetricFamily
    if metric_type == "info":
        c = InfoMetricFamily
    # elif metric_type == "summary":
    #     c = SummaryMetricFamily
    # elif metric_type == "histogram":
    #     c = HistogramMetricFamily

    metric = c(name, documentation or "No Documentation", labels=label_names)
    metric.add_metric([str(labels[k]) for k in label_names], value)

    return metric
