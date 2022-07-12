# gpu_exporter

Collect data about GPUs and exposes them for Prometheus

## Table of Contents

- [gpu_exporter](#gpu_exporter)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Maintainers](#maintainers)
  - [License](#license)

## Usage
> 💡  [More information on poetry](https://python-poetry.org/docs/)


```sh
# install dependencies
$ poetry install

# shell into project
$ poetry shell
```

```sh
$ gpu-exporter --help
Usage: gpu-exporter [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  exporter  Run exporter
```

```sh
$ gpu-exporter exporter --help
Usage: gpu-exporter exporter [OPTIONS]

  Run exporter

Options:
  -m, --mode [server|textfile|pushgateway|stdout]
                                  [default: server]
  -tf, --textfile TEXT            textfile location  [default: /var/lib/node_e
                                  xporter/textfile_collector/gpu_exporter.prom
                                  ]
  -p, --port INTEGER              server port  [default: 9235]
  -pu, --push-url TEXT            pushgateway url  [default: localhost:9091]
  --push-user TEXT                pushgateway username
  --push-pass TEXT                pushgateway password
  --push-job-id TEXT              pushgateway suffix for job name
  -i, --interval INTEGER          Interval in seconds for scraping metrics
  --nvidia                        Enable Nvidia metrics
  --amd                           Enable AMD metrics
  -l, --label <TEXT TEXT>...
  --help                          Show this message and exit.  
```

Exposes metrics API on 0.0.0.0:9235 by default

## Maintainers

[@mezerotm](https://github.com/mezerotm)

## License

© 2022 Cloud Minders