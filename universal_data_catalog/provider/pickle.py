import pickle
from typing import Any

from universal_data_catalog.constants import ReservedKeys

from .base_provider import BaseProvider


class PickleData(BaseProvider):
    """``PickleData`` loads/saves any python object in a pickle format."""

    def load(self) -> Any:
        """Load object using ``pickle.load``.

        Returns:
            Loaded python object
        """
        assert ReservedKeys.FILEPATH in self.config
        with open(self.config[ReservedKeys.FILEPATH], "rb") as f:
            return pickle.load(f)

    def save(self, value: Any) -> None:
        """Save object using ``pickle.dump``."""
        assert ReservedKeys.FILEPATH in self.config
        with open(self.config[ReservedKeys.FILEPATH], "wb") as f:
            pickle.dump(value, f, **self.config.get("load_args", {}))
