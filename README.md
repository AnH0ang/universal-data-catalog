# universal-data-catalog

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

## How to use it ?

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