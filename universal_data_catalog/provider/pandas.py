import pandas as pd

from universal_data_catalog.constants import ReservedKeys

from .base_provider import BaseProvider


class CSVDataSet(BaseProvider):
    """``CSVDataSet`` loads/saves data from/to a CSV file using pandas.

    It acts a thin abstraction layer for the pandas functions ``pd.read_csv``
    and ``pd.DataFrame.to_csv``.
    """

    def load(self) -> pd.DataFrame:
        """Load data using ``pd.read_csv``.

        Returns:
            Loaded DataFrame.
        """
        assert ReservedKeys.FILEPATH in self.config
        return pd.read_csv(
            self.config[ReservedKeys.FILEPATH], **self.config.get("load_args", {})
        )  # type: ignore

    def save(self, value: pd.DataFrame) -> None:
        """Save data using ``pd.DataFrame.to_csv``."""
        assert isinstance(value, pd.DataFrame)
        assert ReservedKeys.FILEPATH in self.config
        value.to_csv(
            self.config[ReservedKeys.FILEPATH], **self.config.get("save_args", {})
        )


class ExcelDataSet(BaseProvider):
    """``ExcelDataSet`` loads/saves data from/to a Excel file using pandas.

    It acts a thin abstraction layer for the pandas functions ``pd.read_excel``
    and ``pd.DataFrame.to_excel``. It uses ``openpyxl`` as a the standard backend.
    """

    def load(self) -> pd.DataFrame:
        """Load data using ``pd.read_excel``.

        Returns:
            Loaded DataFrame.
        """
        assert ReservedKeys.FILEPATH in self.config
        return pd.read_excel(
            self.config[ReservedKeys.FILEPATH], **self.config.get("load_args", {})
        )  # type: ignore

    def save(self, value: pd.DataFrame) -> None:
        """Save data using ``pd.DataFrame.to_excel``."""
        assert isinstance(value, pd.DataFrame)
        assert ReservedKeys.FILEPATH in self.config
        value.to_excel(
            self.config[ReservedKeys.FILEPATH], **self.config.get("save_args", {})
        )
