from prometheus_client.core import (
    CounterMetricFamily,
    GaugeMetricFamily,
    InfoMetricFamily,
)


def make_metric(name, documentation, value=None, metric_type="counter", **labels):
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

    c = CounterMetricFamily

    if metric_type == "gauge":
        c = GaugeMetricFamily
    if metric_type == "info":
        c = InfoMetricFamily

    label_names = list(labels.keys())

    metric = c(name, documentation or "No Documentation", labels=label_names)

    if value != None:
        metric.add_metric([str(labels[k]) for k in label_names], value)

    return metric


def add_metric(metric, value, **labels):
    label_names = list(labels.keys())
    metric.add_metric([str(labels[k]) for k in label_names], value)

    return metric
