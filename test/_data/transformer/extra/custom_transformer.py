from __future__ import annotations

import os

import pandas as pd

from universal_data_catalog.constants import ReservedKeys
from universal_data_catalog.transformer.base_transformer import BaseTransformer
from universal_data_catalog.types import ConfigDict


class AddColumnTransformer(BaseTransformer):
    def after_load(self, value: pd.DataFrame) -> pd.DataFrame:
        assert isinstance(value, pd.DataFrame)
        value["new_col"] = "test1"
        return value

    def before_save(
        self, config: ConfigDict, value: pd.DataFrame
    ) -> tuple[ConfigDict, pd.DataFrame]:
        value["new_col"] = "test2"
        return config, value


class ModifyPathTransformer(BaseTransformer):
    def before_load(self, config: ConfigDict) -> ConfigDict:
        assert ReservedKeys.FILEPATH in config
        config[ReservedKeys.FILEPATH] = os.path.join(
            "data", config[ReservedKeys.FILEPATH]
        )
        return config
