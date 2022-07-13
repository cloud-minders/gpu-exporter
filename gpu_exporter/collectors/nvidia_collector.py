from py3nvml import py3nvml as nvml
from gpu_exporter.libs.utils import make_metric, add_metric
from gpu_exporter.config.events_emitter import emitter
from collections import OrderedDict


class NvidiaCollector(object):
    def __init__(self, nv, custom_labels):
        self.custom_labels = custom_labels
        self.prefix = "nvidia_"
        self.nv = nv
        self.devices = [
            nv.nvmlDeviceGetHandleByIndex(i) for i in range(nv.nvmlDeviceGetCount())
        ]

    def collect(self):
        emitter.emit("logger.debug", msg="collecting from NvidiaCollector")
        metrics = []

        labels = {
            "driver": self.nv.nvmlSystemGetDriverVersion(),
            "gpu": "",
            "gpu_name": "",
        }

        for i in range(len(self.custom_labels)):
            labels[self.custom_labels[i][0]] = self.custom_labels[i][1]

        metric_memused = make_metric(
            self.prefix + "gpu_memory_bytes_used",
            "Used GPU Memory",
            None,
            "gauge",
            **labels,
        )

        metric_memtotal = make_metric(
            self.prefix + "gpu_memory_bytes_total",
            "Total GPU Memory",
            None,
            "gauge",
            **labels,
        )

        metric_powertotal = make_metric(
            self.prefix + "gpu_power_watts",
            "GPU Power Utilization",
            None,
            "gauge",
            **labels,
        )

        metric_temp = make_metric(
            self.prefix + "gpu_temp_celsius", "GPU Temperature", None, "gauge", **labels
        )

        metric_utilpct = make_metric(
            self.prefix + "gpu_usage_ratio",
            "GPU Usage Percentage",
            None,
            "gauge",
            **labels,
        )

        device_labels = []
        for i, device in enumerate(self.devices):
            dl = {}
            dl["gpu"] = f"gpu{i}"
            dl["gpu_name"] = self.nv.nvmlDeviceGetName(device)
            device_labels.append(dl)

        for device, dl in zip(self.devices, device_labels):
            _labels = {**labels, **dl}

            mem_info = self.nv.nvmlDeviceGetMemoryInfo(device)

            add_metric(metric_memused, mem_info.used, **_labels)
            add_metric(metric_memtotal, mem_info.total, **_labels)

            temp_info = 0
            try:
                temp_info = self.nv.nvmlDeviceGetTemperature(
                    device, self.nv.NVML_TEMPERATURE_GPU
                )
            except self.nv.NVMLError_NotSupported:
                temp_info = -1

            add_metric(metric_temp, temp_info, **_labels)

            powertotal = self.nv.nvmlDeviceGetPowerUsage(device) / 1000
            add_metric(metric_powertotal, powertotal, **_labels)

            utilpct = self.nv.nvmlDeviceGetUtilizationRates(device).gpu
            add_metric(metric_utilpct, utilpct, **_labels)

        metrics.extend(
            [
                metric_memused,
                metric_memtotal,
                metric_temp,
                metric_powertotal,
                metric_utilpct,
            ]
        )

        return metrics
