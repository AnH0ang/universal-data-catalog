# Custom Provider

In this chapter, we will create a custom provider that reads a json object as a pandas data frame.

## Folder Structure


```
├── catalog.yml
├── main.py
├── data
│   └── dataset.json
└── src
    ├── __init__.py
    └── custom_provider.py
```

## Subclass `BaseProvider`

* You must implement `.load()` and `.save()`.
* All arguments of the record from `catalog.yml` are loaded into `self.config`.

```python
# src/custom_provider/json_provider.py

import pandas as pd

from universal_data_catalog.provider.base_provider import BaseProvider


class JSONDataSet(BaseProvider):
    def load(self) -> pd.DataFrame:
        return pd.read_json(
            self.config["filepath"], **self.config.get("load_args", {})
        )

    def save(self, value: pd.DataFrame) -> None:
        value.to_json(self.config["filepath"], **self.config.get("save_args", {}))
```

## Integrate into `config.yml`

```yaml
# catalog.yml

json_dataset:
  filepath: dataset.json
  type: src.custom_provider.JSONDataSet
```

## Load from data catalog

```python
# main.py

from universal_data_catalog.data_catalog import DataCatalog

catalog = DataCatalog("catalog.yml", conf)
df = catalog.load("json_dataset")
```
