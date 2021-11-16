import abc
from typing import Any

from universal_data_catalog.types import ConfigDict


class BaseProvider(abc.ABC):
    def __init__(self, config: ConfigDict, **kwargs: Any) -> None:
        self.config = config

    @abc.abstractmethod
    def load(self) -> Any:
        pass

    @abc.abstractmethod
    def save(self, value: Any) -> None:
        pass
