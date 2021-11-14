# universal-data-catalog

[![Documentation Status](https://readthedocs.org/projects/universal-data-catalog/badge/?version=latest)](https://universal-data-catalog.readthedocs.io/en/latest/?badge=latest)
![example workflow](https://github.com/AnH0ang/universal-data-catalog/actions/workflows/github-actions-demo.yml/badge.svg)
[![codecov](https://codecov.io/gh/AnH0ang/universal-data-catalog/branch/github-actions-test/graph/badge.svg?token=UKXBKOXDVQ)](https://codecov.io/gh/AnH0ang/universal-data-catalog)
[![PyPI version](https://badge.fury.io/py/universal-data-catalog.svg)](https://badge.fury.io/py/universal-data-catalog)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/AnH0ang/universal-data-catalog/blob/master/LICENCE)
[![Maintainability](https://api.codeclimate.com/v1/badges/b5bc602f4fb7c1132715/maintainability)](https://codeclimate.com/github/AnH0ang/universal-data-catalog/maintainability)
[![Python version](https://img.shields.io/badge/python->=3.7-blue.svg)](https://pypi.org/project/kedro/)

## What is `universal-data-catalog` ?

The goal of `universal-data-catalog` is to act as abstaction layer on data IO targeted at small to medium sized data science projects.
Instead of hard codeding data interface in `pandas`, the configuration is instead loaded from a config file which acts as a data catalog. The concept is borrowed from [kedro](https://github.com/quantumblacklabs/kedro) data catalogs.

## Why use it ?
* Instead of hardcoding it or relying of command line arguments use a config file.
* itegrate easy with `hydra` and other `yaml` based configuration/orchestration tools.
* simple interface (less that 50 lines of code)
* customizable
* Wide ecosystem with wide range of providers
    * `pandas`
    * `networkx`
    * `snowflake` (planned)
    * `azure blob` (planned)
    * `aws s3` (planned)

## Installation

```
pip install universal-data-catalog
```

## Usage 

```yaml
# catalog.yml

titanic:
  filepath: titanic.csv
  type: pandas.CSVDataSet
  load_args:
    sep: ","
```

```python
# main.py

from universal_data_catalog.data_catalog import DataCatalog

catalog = DataCatalog("catalog.yml", conf)
titanic_df = catalog.load("titanic")
```
