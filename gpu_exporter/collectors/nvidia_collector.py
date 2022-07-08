from py3nvml import py3nvml as nvml
from gpu_exporter.libs.utils import make_metric
import re


class NvidiaCollector(object):
    def __init__(self, nv, custom_labels):
        self.custom_labels = custom_labels
        self.prefix = "nvidia_"
        self.nv = nv
        self.devices = [
            nv.nvmlDeviceGetHandleByIndex(i) for i in range(nv.nvmlDeviceGetCount())
        ]

    def collect(self):
        metrics = []

        ids = {"driver": self.nv.nvmlSystemGetDriverVersion()}

        for i in range(len(self.custom_labels)):
            ids[self.custom_labels[i][0]] = self.custom_labels[i][1]

        for i, device in enumerate(self.devices):
            ids["gpu"] = f"gpu{i}"
            ids["gpu_name"] = self.nv.nvmlDeviceGetName(device)

            mem_info = self.nv.nvmlDeviceGetMemoryInfo(device)

            metrics.append(
                make_metric(
                    self.prefix + "gpu_memory_bytes_used",
                    "Used GPU Memory",
                    mem_info.used,
                    "gauge",
                    **ids,
                )
            )

            metrics.append(
                make_metric(
                    self.prefix + "gpu_memory_bytes_total",
                    "Total GPU Memory",
                    mem_info.total,
                    "gauge",
                    **ids,
                )
            )

            temp_info = 0
            try:
                temp_info = self.nv.nvmlDeviceGetTemperature(
                    device, self.nv.NVML_TEMPERATURE_GPU
                )
            except self.nv.NVMLError_NotSupported:
                temp_info = -1

            metrics.append(
                make_metric(
                    self.prefix + "gpu_temp_celsius",
                    "GPU Temperature",
                    temp_info,
                    "gauge",
                    **ids,
                )
            )

            metrics.append(
                make_metric(
                    self.prefix + "gpu_power_watts",
                    "GPU Power Utilization",
                    self.nv.nvmlDeviceGetPowerUsage(device) / 1000,
                    "gauge",
                    **ids,
                )
            )

            metrics.append(
                make_metric(
                    self.prefix + "gpu_usage_ratio",
                    "GPU Usage Percentage",
                    self.nv.nvmlDeviceGetUtilizationRates(device).gpu,
                    "gauge",
                    **ids,
                )
            )

        return metrics
