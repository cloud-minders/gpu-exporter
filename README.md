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

# path #1: Install on system
$ poetry build
$ pip install dist/gpu_exporter-<version>.tar.gz
$ gpu-exporter --help

# path #2: Use in virtualenv
# shell into project
$ poetry shell
```

## Maintainers

[@mezerotm](https://github.com/mezerotm)

## License

© 2022 Cloud Minders