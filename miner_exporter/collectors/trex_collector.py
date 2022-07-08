import requests
from miner_exporter.libs.utils import make_metric


class TrexCollector(object):
    def __init__(self, url, custom_labels):
        self.url = url
        self.custom_labels = custom_labels
        self._prefix = "trex_"

    def collect(self):
        metrics = []

        j = requests.get(self.url).json()
        ids = {
            "user": j["active_pool"]["user"],
            "worker_id": j["active_pool"]["worker"],
        }

        for i in range(len(self.custom_labels)):
            ids[self.custom_labels[i][0]] = self.custom_labels[i][1]

        count = 0
        for gpu in j["gpus"]:
            labels = {
                "gpu_name": gpu["name"],
                "vendor": gpu["vendor"],
            }
            labels.update(ids)
            metrics.append(
                make_metric(
                    self._prefix + f"gpu_hashrate{count}",
                    "GPU Hashrate",
                    gpu["hashrate"],
                    "gauge",
                    **labels,
                )
            )
            count += 1

        metrics.append(
            make_metric(
                self._prefix + "hashrate_total",
                "Overall Hashrate",
                j["hashrate"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "hashrate_day",
                "Hashrate in day",
                j["hashrate_day"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "hashrate_hour",
                "Hashrate in hour",
                j["hashrate_hour"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "hashrate_minute",
                "Hashrate in minute",
                j["hashrate_minute"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "gpu_total", "Total gpus", j["gpu_total"], "gauge", **ids
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "sharerate", "Sharerate", j["sharerate"], "gauge", **ids
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "sharerate_average",
                "Average Sharerate",
                j["sharerate_average"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "pool_accepted_shares",
                "Pool accepted shares",
                j["accepted_count"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "pool_rejected_shares",
                "Pool rejected shares",
                j["rejected_count"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "pool_last_submit_ts",
                "Pool last sumbit timestamp",
                j["active_pool"]["last_submit_ts"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "pool_ping",
                "Pool ping",
                j["active_pool"]["ping"],
                "gauge",
                **ids,
            )
        )

        # metrics.append(
        #     make_metric(
        #         self._prefix + "gpu_driver", "NVIDIA driver", j["driver"], "info", **ids
        #     )
        # )

        # metrics.append(
        #     make_metric(self._prefix + "os", "Operating System", j["os"], "info", **ids)
        # )

        # metrics.append(
        #     make_metric(
        #         self._prefix + "algorithm", "Algorithm", j["algorithm"], "info", **ids
        #     )
        # )

        # metrics.append(
        #     make_metric(
        #         self._prefix + "pool_url",
        #         "Pool url",
        #         j["active_pool"]["url"],
        #         "info",
        #         **ids
        #     )
        # )

        # metrics.append(
        #     make_metric(
        #         self._prefix + "pool_user",
        #         "Pool user",
        #         j["active_pool"]["user"],
        #         "info",
        #         **ids
        #     )
        # )

        return metrics


# {
#   "accepted_count": 1,
#   "active_pool": {
#     "difficulty": "4.29 G",
#     "dns_https_server": "",
#     "last_submit_ts": 1655999199,
#     "ping": 33,
#     "proxy": "",
#     "retries": 0,
#     "url": "stratum+tcp://us1.ethermine.org:4444",
#     "user": "0x4EEB2D6Ec9cd842a13ab24c013b7a7A66F6AC2B4",
#     "worker": ""
#   },
#   "algorithm": "ethash",
#   "api": "4.1",
#   "build_date": "Mar 16 2022 07:01:51",
#   "coin": "",
#   "description": "T-Rex NVIDIA GPU miner",
#   "driver": "470.86",
#   "gpu_total": 1,
#   "gpus": [
#     {
#       "cclock": 1935,
#       "dag_build_mode": 0,
#       "device_id": 0,
#       "efficiency": "259kH/W",
#       "fan_speed": 68,
#       "gpu_id": 0,
#       "gpu_user_id": 0,
#       "hashrate": 50287688,
#       "hashrate_day": 50288326,
#       "hashrate_hour": 50288326,
#       "hashrate_instant": 51142920,
#       "hashrate_minute": 50287688,
#       "intensity": 22,
#       "lhr_lock_count": 0,
#       "lhr_tune": 0,
#       "low_load": true,
#       "mclock": 6800,
#       "mtweak": 0,
#       "name": "RTX 3070",
#       "paused": false,
#       "pci_bus": 10,
#       "pci_domain": 0,
#       "pci_id": 0,
#       "potentially_unstable": false,
#       "power": 195,
#       "power_avr": 194,
#       "shares": {
#         "accepted_count": 1,
#         "invalid_count": 0,
#         "last_share_diff": 0,
#         "last_share_submit_ts": 0,
#         "max_share_diff": 0,
#         "max_share_submit_ts": 0,
#         "rejected_count": 0,
#         "solved_count": 0
#       },
#       "temperature": 74,
#       "uuid": "3e95c8ebee1ca0d490c7a000a27f4c55",
#       "vendor": "NVIDIA"
#     }
#   ],
#   "hashrate": 50287688,
#   "hashrate_day": 50288326,
#   "hashrate_hour": 50288326,
#   "hashrate_minute": 50287688,
#   "invalid_count": 0,
#   "name": "t-rex",
#   "os": "linux",
#   "paused": false,
#   "rejected_count": 0,
#   "revision": "fcd1d0561127",
#   "sharerate": 1,
#   "sharerate_average": 1.714,
#   "solved_count": 0,
#   "success": 1,
#   "time": 1655999280,
#   "uptime": 116,
#   "validate_shares": false,
#   "version": "0.25.9",
#   "watchdog_stat": {
#     "built_in": true,
#     "startup_ts": 10468,
#     "total_restarts": 0,
#     "uptime": 117,
#     "wd_version": "0.25.9"
#   }
# }
