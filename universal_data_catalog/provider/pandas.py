import pandas as pd

from universal_data_catalog.constants import ReservedKeys

from .base_provider import BaseProvider


class CSVDataSet(BaseProvider):
    def load(self) -> pd.DataFrame:
        assert ReservedKeys.FILEPATH in self.config
        return pd.read_csv(
            self.config[ReservedKeys.FILEPATH], **self.config.get("load_args", {})
        )  # type: ignore

    def save(self, value: pd.DataFrame) -> None:
        assert isinstance(value, pd.DataFrame)
        assert ReservedKeys.FILEPATH in self.config
        value.to_csv(
            self.config[ReservedKeys.FILEPATH], **self.config.get("save_args", {})
        )


class ExcelDataSet(BaseProvider):
    def load(self) -> pd.DataFrame:
        assert ReservedKeys.FILEPATH in self.config
        return pd.read_excel(
            self.config[ReservedKeys.FILEPATH], **self.config.get("load_args", {})
        )  # type: ignore

    def save(self, value: pd.DataFrame) -> None:
        assert isinstance(value, pd.DataFrame)
        assert ReservedKeys.FILEPATH in self.config
        value.to_excel(
            self.config[ReservedKeys.FILEPATH], **self.config.get("save_args", {})
        )
