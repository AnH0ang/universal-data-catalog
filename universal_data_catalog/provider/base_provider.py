import abc
from typing import Any

from universal_data_catalog.types import ConfigDict


class BaseProvider(abc.ABC):
    """A base class for dataset providers that implements read and save operations."""

    def __init__(self, config: ConfigDict, **kwargs: Any) -> None:
        """Initialize the provider.

        Args:
            config: Configuration that is passed from the yaml config file.
        """
        self.config = config

    @abc.abstractmethod
    def load(self) -> Any:
        """The method that is used to load the data.

        Returns:
            Loaded Data.
        """
        pass

    @abc.abstractmethod
    def save(self, value: Any) -> None:
        """The method that is used to save the data to the specified value.

        Args:
            value: Value that will be saved.
        """
        pass
