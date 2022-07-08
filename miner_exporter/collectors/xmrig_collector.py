import requests
from miner_exporter.libs.utils import make_metric


class XmrigCollector(object):
    def __init__(self, url, custom_labels):
        self.url = url
        self.custom_labels = custom_labels
        self._prefix = "xmrig_"

    def collect(self):
        metrics = []

        j = requests.get(self.url).json()
        ids = {}

        for i in range(len(self.custom_labels)):
            ids[self.custom_labels[i][0]] = self.custom_labels[i][1]

        for i, v in enumerate(j["hashrate"]["total"]):
            if v is not None:
                metrics.append(
                    make_metric(
                        self._prefix + f"hashrate{i}",
                        "Overall Hashrate",
                        v,
                        "gauge",
                        **ids,
                    )
                )

        # for tidx, t in enumerate(j["hashrate"]["threads"]):
        #     for i, v in enumerate(t):
        #         if not v is None:
        #             labels = {"thread": tidx}
        #             labels.update(ids)
        #             metrics.append(
        #                 make_metric(
        #                     self._prefix + "thread_hashrate%d" % i,
        #                     "Thread Hashrate",
        #                     v,
        #                     "gauge",
        #                     **labels
        #                 )
        #             )

        metrics.append(
            make_metric(
                self._prefix + "diff_current",
                "Current Difficulty",
                j["results"]["diff_current"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "shares_good",
                "Good Shares",
                j["results"]["shares_good"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "shares_total",
                "Total Shares",
                j["results"]["shares_total"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "avg_time",
                "Average Time",
                j["results"]["avg_time"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "hashes_total",
                "Total Hashes",
                j["results"]["hashes_total"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "best", "Best", j["results"]["best"][0], "gauge", **ids
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "errors",
                "Count of errors",
                len(j["results"]["error_log"]),
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "connection_uptime",
                "Connection uptime",
                j["connection"]["uptime"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "connection_ping",
                "Connection ping",
                j["connection"]["ping"],
                "gauge",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "connection_failures",
                "Connection failures",
                j["connection"]["failures"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "pool_accepted_shares",
                "Pool accepted shares",
                j["connection"]["accepted"],
                "counter",
                **ids,
            )
        )

        metrics.append(
            make_metric(
                self._prefix + "pool_rejected_shares",
                "Pool rejected shares",
                j["connection"]["rejected"],
                "counter",
                **ids,
            )
        )

        return metrics


# {
#   "id": "95b4c3432f64173a",
#   "worker_id": "crincon",
#   "uptime": 11,
#   "restricted": true,
#   "resources": {
#     "memory": {
#       "free": 47044018176,
#       "total": 58898145280,
#       "resident_set_memory": 2530295808
#     },
#     "load_average": [
#       3.14,
#       0.95,
#       0.53
#     ],
#     "hardware_concurrency": 16
#   },
#   "features": [
#     "api",
#     "asm",
#     "http",
#     "hwloc",
#     "tls",
#     "opencl",
#     "cuda"
#   ],
#   "results": {
#     "diff_current": 480045,
#     "shares_good": 0,
#     "shares_total": 0,
#     "avg_time": 0,
#     "avg_time_ms": 0,
#     "hashes_total": 0,
#     "best": [
#       0,
#       0,
#       0,
#       0,
#       0,
#       0,
#       0,
#       0,
#       0,
#       0
#     ],
#     "error_log": []
#   },
#   "algo": "rx/0",
#   "connection": {
#     "pool": "xmr-us-east1.nanopool.org:14433",
#     "ip": "144.217.14.139",
#     "uptime": 11,
#     "uptime_ms": 11321,
#     "ping": 0,
#     "failures": 0,
#     "tls": "TLSv1.2",
#     "tls-fingerprint": "c38886efdee542ebd99801b75c75d3498d97978bbcdec07c7271cb19729e014f",
#     "algo": "rx/0",
#     "diff": 480045,
#     "accepted": 0,
#     "rejected": 0,
#     "avg_time": 0,
#     "avg_time_ms": 0,
#     "hashes_total": 0,
#     "error_log": []
#   },
#   "version": "6.17.0",
#   "kind": "miner",
#   "ua": "XMRig/6.17.0 (Linux x86_64) libuv/1.40.0 gcc/9.3.0",
#   "cpu": {
#     "brand": "AMD Ryzen 7 3700X 8-Core Processor",
#     "family": 23,
#     "model": 113,
#     "stepping": 0,
#     "proc_info": 8851216,
#     "aes": true,
#     "avx2": true,
#     "x64": true,
#     "64_bit": true,
#     "l2": 4194304,
#     "l3": 33554432,
#     "cores": 8,
#     "threads": 16,
#     "packages": 1,
#     "nodes": 1,
#     "backend": "hwloc/2.4.1",
#     "msr": "ryzen_17h",
#     "assembly": "ryzen",
#     "arch": "x86_64",
#     "flags": [
#       "aes",
#       "avx",
#       "avx2",
#       "bmi2",
#       "osxsave",
#       "pdpe1gb",
#       "sse2",
#       "ssse3",
#       "sse4.1",
#       "popcnt",
#       "cat_l3"
#     ]
#   },
#   "donate_level": 1,
#   "paused": false,
#   "algorithms": [
#     "cn/1",
#     "cn/2",
#     "cn/r",
#     "cn/fast",
#     "cn/half",
#     "cn/xao",
#     "cn/rto",
#     "cn/rwz",
#     "cn/zls",
#     "cn/double",
#     "cn/ccx",
#     "cn-lite/1",
#     "cn-heavy/0",
#     "cn-heavy/tube",
#     "cn-heavy/xhv",
#     "cn-pico",
#     "cn-pico/tlo",
#     "cn/upx2",
#     "rx/0",
#     "rx/wow",
#     "rx/arq",
#     "rx/graft",
#     "rx/sfx",
#     "rx/keva",
#     "argon2/chukwa",
#     "argon2/chukwav2",
#     "argon2/ninja",
#     "astrobwt",
#     "astrobwt/v2",
#     "ghostrider"
#   ],
#   "hashrate": {
#     "total": [
#       null,
#       null,
#       null
#     ],
#     "highest": null,
#     "threads": [
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ],
#       [
#         null,
#         null,
#         null
#       ]
#     ]
#   },
#   "hugepages": false
# }
