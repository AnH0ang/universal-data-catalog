# Custom Transformer

In this example, we will create a transformer that creates a new column before storing the data in the data catalog.


## Folder Structure

```
├── catalog.yml
├── main.py
├── data
│   └── titanic.csv
└── src
    ├── __init__.py
    └── custom_transformer.py
```

## Subclass `BaseTransformer`

* You can implement any of `.before_load()`, `.after_load()` or `before_save()`.
* All arguments of the transformer from `catalog.yml` are loaded into `self.config`.



```python
import pandas as pd

from universal_data_catalog.types import ConfigDict
from universal_data_catalog.transformer.base_transformer import BaseTransformer

class AddColumnTransformer(BaseTransformer):
    def before_load(self, data_config: ConfigDict) -> ConfigDict:
        # you can change the data_config before is passed to the provider
        return data_config

    def after_load(self, value: pd.DataFrame) -> pd.DataFrame:
        # add a new column after you load the dataset
        value[self.config["col"]] = self.config["val"]
        return value

    def before_save(
        self, config: ConfigDict, value: pd.DataFrame
    ) -> tuple[ConfigDict, pd.DataFrame]:
        # add a new column before the data is save to the disk
        value[self.config["col"]] = self.config["val"]
        return config, value
```

## Integrate into `config.yml`

```yaml
# catalog.yml

titanic:
  filepath: dataset.json
  type: pandas.CSVDataSet
  transformer:
    - type: src.custom_transformer.AddColumnTransformer
      col: "new_col"
      val: "new_val"
```


## Load from data catalog

```python
# main.py

from universal_data_catalog.data_catalog import DataCatalog

catalog = DataCatalog("catalog.yml", conf)
df = catalog.load("titanic")
assert (df["new_col"] == "new_val").all()
```
