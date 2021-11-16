# universal-data-catalog


[![Documentation Status](https://readthedocs.org/projects/universal-data-catalog/badge/?version=latest)](https://universal-data-catalog.readthedocs.io/en/latest/?badge=latest)
![release workflow](https://github.com/AnH0ang/universal-data-catalog/actions/workflows/release.yml/badge.svg)
![test workflow](https://github.com/AnH0ang/universal-data-catalog/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/AnH0ang/universal-data-catalog/branch/master/graph/badge.svg?token=UKXBKOXDVQ)](https://codecov.io/gh/AnH0ang/universal-data-catalog)
[![PyPI version](https://badge.fury.io/py/universal-data-catalog.svg)](https://badge.fury.io/py/universal-data-catalog)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/AnH0ang/universal-data-catalog/blob/master/LICENCE)
[![Maintainability](https://api.codeclimate.com/v1/badges/b5bc602f4fb7c1132715/maintainability)](https://codeclimate.com/github/AnH0ang/universal-data-catalog/maintainability)
[![Python version](https://img.shields.io/badge/python-3.7|3.8|3.9-blue.svg)](https://pypi.org/project/kedro/)


## Introduction

The goal of `universal-data-catalog` is to act as an abstraction layer on top of data IO targeted
at small to medium sized Data Science projects.
Rather than hard-coding the data interface in `pandas`, the configuration is instead loaded
from a configuration file that acts as a data catalog.
The concept is borrowed from [kedro](https://github.com/quantumblacklabs/kedro) data catalog.

Full documentation can be found at [readthedocs.com](https://universal-data-catalog.readthedocs.io/en/latest/).

## Why use it ?

The advantages of `universal-data-catalog` are:
* **Abstraction**: Instead of hard-coding the data interface, you can use a configuration file
that separates the code from the configuration.
* **YAML-Config**: Since the configuration file is in `YAML` format, it can be easily integrated
with `Hydra` and other `YAML` based configuration/orchestration tools.
* **Customizability**: Link your own data provider to the data catalog.
* **Plugable**: A wide range of providers are supported and many more will be added. Those include:
    * `pandas`
    * `networkx`
    * `pickle`
    * `snowflake` (planned)
    * `azure blob` (planned)
    * `aws s3` (planned)

## Installation

You can easily install this package using `pip`.

```
pip install universal-data-catalog
```

## Usage

Specify the loading configuration for your data in a separate `config.yaml` file.

```yaml
# catalog.yml

titanic:
  filepath: titanic.csv
  type: pandas.CSVDataSet
  load_args:
    sep: ","
```

Load the dataset from Python via the data catalog.

```python
# main.py

from universal_data_catalog.data_catalog import DataCatalog

catalog = DataCatalog("catalog.yml", conf)
titanic_df = catalog.load("titanic")
```
