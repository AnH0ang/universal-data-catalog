import pickle
from typing import Any

from universal_data_catalog.constants import ReservedKeys

from .base_provider import BaseProvider


class PickleData(BaseProvider):
    def save(self, value: Any) -> None:
        assert ReservedKeys.FILEPATH in self.config
        with open(self.config[ReservedKeys.FILEPATH], "wb") as f:
            pickle.dump(value, f, **self.config.get("load_args", {}))

    def load(self) -> Any:
        assert ReservedKeys.FILEPATH in self.config
        with open(self.config[ReservedKeys.FILEPATH], "rb") as f:
            return pickle.load(f)
