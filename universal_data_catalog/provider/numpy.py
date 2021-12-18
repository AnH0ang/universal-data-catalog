import numpy as np

from universal_data_catalog.constants import ReservedKeys

from .base_provider import BaseProvider


class NumpyArray(BaseProvider):
    """``NumpyArray`` loads/saves a numpy from/to a npy file.

    It acts a thin abstraction layer for the numpy functions ``np.load``
    and ``np.save``.
    """

    def load(self) -> np.ndarray:
        """Load data using ``np.load``.

        Returns:
            Loaded numpy array.
        """
        assert ReservedKeys.FILEPATH in self.config
        with open(self.config[ReservedKeys.FILEPATH], "rb") as f:
            return np.load(f, **self.config.get("load_args", {}))  # type: ignore

    def save(self, value: np.ndarray) -> None:
        """Save data using ``np.save``."""
        assert isinstance(value, np.ndarray)
        assert ReservedKeys.FILEPATH in self.config
        with open(self.config[ReservedKeys.FILEPATH], "wb") as f:
            np.save(f, value, **self.config.get("save_args", {}))
